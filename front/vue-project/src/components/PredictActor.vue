<template>
  <div class="page-container">
    <div class="teachable-machine">
      <section class="teachable-title">
        <h2 class="text-xl mb-4">나의 닮은꼴 배우 찾기</h2>
        <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded">
          {{ error }}
        </div>
      </section>
      <div class="teachable-content">
        <section class="upload-img-container">
          <h3 class="mb-3">얼굴 사진을 올려주세요</h3>
          <input
            type="file"
            @change="handleImageUpload"
            accept="image/*"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <div v-if="imageUrl" class="img-container">
            <img
              ref="imagePreview"
              :src="imageUrl"
              alt="uploaded image"
              @load="analyzeImage"
            />
          </div>
          <div v-else class="none-img-container">이미지를 업로드해주세요.</div>
        </section>
        <section v-if="topPrediction" class="moveto-container">
          <div class="container">
            <div class="arrow"></div>
          </div>
        </section>
        <section class="result-container">
          <h3 class="mb-3">당신이 닮은 배우는?</h3>
          <div v-if="topPrediction" class="done-predict">
            <p class="actor-predict">
              {{ topPrediction.className }} -
              {{ (topPrediction.probability * 100).toFixed(2) }}%
            </p>
            <h4 class="font-bold mt-4 movie-info-title">출연 영화</h4>
            <ul v-if="movies.length > 0">
              <li v-for="movie in movies" :key="movie.id">
                {{ movie.title }} ({{
                  new Date(movie.release_date).getFullYear()
                }})
              </li>
            </ul>
            <p v-else class="mt-5">출연 영화 정보를 찾을 수 없습니다.</p>
          </div>
          <div v-else class="yet-predict">
            <p>이미지를 업로드하고 분석을 시작해주세요.</p>
          </div>
        </section>
      </div>
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
const topPrediction = ref(null);
const movies = ref([]);

let model = null;
const modelPath = ref("/models/my-model/");

// 이미지 리사이즈 함수
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

// 이미지 업로드 처리
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

// 이미지 분석
const analyzeImage = async () => {
  if (!model || !imagePreview.value) {
    error.value = "모델이 준비되지 않았습니다.";
    return;
  }

  try {
    console.log("이미지 분석 시작");
    const results = await model.predict(imagePreview.value);
    predictions.value = results.sort((a, b) => b.probability - a.probability);

    if (predictions.value.length > 0) {
      topPrediction.value = predictions.value[0];
      console.log("닮은 배우 예측:", topPrediction.value);

      const actorId = getActorId(topPrediction.value?.className);
      console.log("TMDB 배우 ID:", actorId);

      if (actorId) {
        movies.value = await getMoviesByActor(actorId);
        console.log("출연 영화 데이터:", movies.value);
      } else {
        error.value = "TMDB에서 배우 정보를 찾을 수 없습니다.";
      }
    }
  } catch (err) {
    error.value = "이미지 분석 중 오류가 발생했습니다.";
    console.error("분석 오류:", err);
  }
};

// 모델 초기화
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
    model = null; // 초기화 실패 시 null 설정
    error.value = "모델을 불러오는 중 오류가 발생했습니다.";
    console.error("모델 로드 오류:", err);
  }
};

// 컴포넌트가 소멸될 때 모델 정리
onUnmounted(() => {
  if (model && typeof model.dispose === "function") {
    model.dispose();
    console.log("모델 정리 완료");
  } else {
    console.log("모델이 초기화되지 않았거나 이미 정리되었습니다.");
  }

  if (window.tf) {
    try {
      window.tf.engine().disposeVariables();
    } catch (err) {
      console.error("TensorFlow.js 변수 정리 중 오류 발생:", err);
    }
  }
});

// 컴포넌트 로드 시 실행
onMounted(async () => {
  try {
    await loadScript(
      "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"
    );
    await loadScript(
      "https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"
    );

    await initModel();
  } catch (err) {
    error.value = "초기화 중 오류가 발생했습니다.";
    console.error("초기화 오류:", err);
  }
});

// 스크립트 동적 로드 함수
const loadScript = (src) => {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
};
</script>

<style scoped>
.page-container {
  color: white;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 4rem;
}

.teachable-machine {
  width: 80%;
  margin-top: 2rem;
}

.teachable-title {
  text-align: center;
  margin-bottom: 2rem;
}

.teachable-content {
  width: 100%;
  min-height: 700px;
  display: flex;
  justify-content: space-between;
}

.upload-img-container {
  width: 40%;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid var(--dark-gray);
  border-radius: 10px;
  padding: 2rem 2rem;
}

.upload-img-container > input {
  margin-bottom: 2rem;
}

.img-container {
  width: 100%;
  min-height: 500px;
}

.img-container img {
  width: 100%;
}

.none-img-container {
  width: 500px;
  min-height: 500px;
  text-align: center;
  padding: 250px 0;
}

.moveto-container {
  height: 750px;
  display: flex;
  align-items: center;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  width: 300px;
  margin: 0 auto;
  overflow: hidden;
  position: relative;
}

.arrow {
  font-size: 24px;
  animation: slideArrow 2s infinite;
  position: absolute;
  opacity: 0;
}

@keyframes slideArrow {
  0% {
    transform: translateX(-100px);
    opacity: 0;
  }

  20% {
    transform: translateX(0);
    opacity: 1;
  }

  80% {
    transform: translateX(0);
    opacity: 1;
  }

  100% {
    transform: translateX(100px);
    opacity: 0;
  }
}

/* CSS 화살표 대신 실제 화살표 문자 사용 */
.arrow::after {
  content: "→";
  font-size: 2rem;
  font-weight: bold;
}

.result-container {
  width: 40%;
  min-height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid var(--dark-gray);
  border-radius: 10px;
  padding: 2rem 2rem;
}

.result-container > h3 {
  text-align: center;
}
.movie-info-title {
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 2rem;
}
.result-container > .done-predict,
.result-container > .yet-predict {
  min-height: 400px;
}
.actor-predict {
  font-size: 1.5rem;
  text-align: center;
  margin: 3rem 0;
  text-decoration: underline;
}
.result-container > .yet-predict {
  padding: 300px 0;
}
</style>
