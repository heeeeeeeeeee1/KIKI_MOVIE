<template>
  <div class="teachable-machine">
    <h2 class="text-xl mb-4">Teachable Machine Image Model</h2>

    <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded">
      {{ error }}
    </div>

    <div class="mb-4">
      <input
        type="file"
        @change="handleImageUpload"
        accept="image/*"
        class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />
    </div>

    <div v-if="imageUrl" class="mb-4">
      <img
        ref="imagePreview"
        :src="imageUrl"
        alt="uploaded image"
        class="max-w-xs rounded shadow"
        @load="analyzeImage"
      />
    </div>

    <div v-if="predictions.length > 0" class="mt-4 p-4 bg-gray-50 rounded">
      <h3 class="font-bold mb-2">닮은 배우 목록:</h3>
      <ul>
        <li v-for="(prediction, index) in predictions" :key="index">
          <p class="text-lg font-semibold">{{ prediction.className }}</p>
          <p class="text-sm">확률: {{ (prediction.probability * 100).toFixed(2) }}%</p>
        </li>
      </ul>
      <h4 class="font-bold mt-4">출연 영화:</h4>
      <ul v-if="movies.length > 0">
        <li v-for="movie in movies" :key="movie.id">
          {{ movie.title }} ({{ new Date(movie.release_date).getFullYear() }})
        </li>
      </ul>
      <p v-else>출연 영화 정보를 찾을 수 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { getActorId } from "../api/actorMapping";
import { getMoviesByActor } from "../api/tmdb";

const error = ref(null);
const imageUrl = ref(null);
const imagePreview = ref(null);
const predictions = ref([]);
const movies = ref([]);

let model = null;
const modelPath = ref("/models/my-model/");

const resizeImage = (file, width, height) => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const reader = new FileReader();

    reader.onload = (event) => {
      img.src = event.target.result;
    };

    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");

      if (!ctx) {
        reject(new Error("2D context를 생성할 수 없습니다."));
        return;
      }

      try {
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            if (blob) {
              resolve(URL.createObjectURL(blob));
            } else {
              reject(new Error("Blob 생성에 실패했습니다."));
            }
          },
          "image/jpeg",
          0.8
        );
      } catch (err) {
        reject(new Error("이미지 처리 중 오류가 발생했습니다: " + err.message));
      }
    };

    img.onerror = () => {
      reject(new Error("이미지 로드 중 오류가 발생했습니다."));
    };
    reader.onerror = () => {
      reject(new Error("파일 읽기 중 오류가 발생했습니다."));
    };

    reader.readAsDataURL(file);
  });
};

const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    error.value = "파일 크기는 5MB 이하여야 합니다.";
    return;
  }

  if (!file.type.startsWith("image/")) {
    error.value = "이미지 파일만 업로드 가능합니다.";
    return;
  }

  error.value = null;

  try {
    console.log("이미지 리사이즈 시작");
    imageUrl.value = await resizeImage(file, 224, 224);
    console.log("이미지 리사이즈 완료");
  } catch (err) {
    error.value = "이미지 리사이즈 중 오류가 발생했습니다: " + err.message;
    console.error("이미지 리사이즈 오류:", err);
  }
};

const analyzeImage = async () => {
  if (!model || !imagePreview.value) {
    error.value = "모델이 준비되지 않았습니다.";
    return;
  }

  try {
    console.log("이미지 분석 시작");
    const results = await model.predict(imagePreview.value);
    predictions.value = results.sort((a, b) => b.probability - a.probability);
    console.log("이미지 분석 완료:", predictions.value);

    if (predictions.value.length > 0) {
      topPrediction.value = predictions.value[0];
      console.log("닮은 배우 예측:", topPrediction.value);

      const actorId = getActorId(topPrediction.value?.className);
      console.log("TMDB 배우 ID:", actorId);

      if (actorId) {
        movies.value = await getMoviesByActor(actorId);
        console.log("출연 영화 데이터:", movies.value);
//      const actorId = getActorId(predictions.value[0]?.className);
//
//      if (actorId) {
//        movies.value = await getMoviesByActor(actorId);
//        console.log("영화 정보 로드 완료:", movies.value);
      } else {
        error.value = "TMDB에서 배우 정보를 찾을 수 없습니다.";
      }
    }
  } catch (err) {
    error.value = "이미지 분석 중 오류가 발생했습니다.";
    console.error("분석 오류:", err);
  }
};

const initModel = async () => {
  if (!window.tmImage) {
    error.value = "Teachable Machine 라이브러리가 아직 로드되지 않았습니다.";
    return;
  }

  try {
    console.log("모델 로드 시작");
    const modelURL = `${modelPath.value}model.json`;
    const metadataURL = `${modelPath.value}metadata.json`;

    model = await window.tmImage.load(modelURL, metadataURL);
    console.log("모델 로드 성공");
  } catch (err) {
    error.value = "모델을 불러오는 중 오류가 발생했습니다.";
    console.error("모델 로드 오류:", err);
  }
};

const loadScript = (src) => {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
};

onUnmounted(() => {
  if (model) {
    model.dispose();
  }

  if (window.tf) {
    try {
      window.tf.engine().disposeVariables();
      console.log("TensorFlow.js 변수 정리 완료");
    } catch (err) {
      console.error("TensorFlow.js 변수 정리 중 오류 발생:", err);
    }
  }
});

onMounted(async () => {
  try {
    console.log("스크립트 로딩 시작");
    await loadScript(
      "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"
    );
    await loadScript(
      "https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"
    );
    console.log("스크립트 로딩 완료");

    await initModel();
  } catch (err) {
    error.value = "초기화 중 오류가 발생했습니다.";
    console.error("초기화 오류:", err);
  }
});
</script>

<style>
.teachable-machine {
  color: white;
}
</style>