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
      <h3 class="font-bold mb-2">분석 결과:</h3>
      <div v-for="(prediction, index) in predictions" :key="index" class="mb-2">
        <div class="flex justify-between items-center">
          <span class="font-medium">{{ prediction.className }}:</span>
          <span>{{ (prediction.probability * 100).toFixed(2) }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded h-2">
          <div
            class="bg-blue-600 rounded h-2"
            :style="{ width: `${prediction.probability * 100}%` }"
          ></div>
        </div>
      </div>

      <!-- 결과 내보내기 버튼 -->
      <div class="mt-4 space-x-2">
        <button
          @click="getFormattedResults('object')"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          객체로 내보내기
        </button>
        <button
          @click="getFormattedResults('array')"
          class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          배열로 내보내기
        </button>
      </div>

      <!-- 결과 출력 영역 -->
      <div v-if="formattedResult" class="mt-4">
        <h4 class="font-bold mb-2">포맷된 결과:</h4>
        <pre class="bg-gray-100 p-4 rounded overflow-x-auto">{{
          formattedResult
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const error = ref(null);
const imageUrl = ref(null);
const imagePreview = ref(null);
const predictions = ref([]);
const formattedResult = ref(null);

let model = null;
// 모델 폴더 경로 설정
const modelPath = ref("/models/my-model/");

// 결과를 객체 또는 배열 형태로 반환하는 함수
function getFormattedResults(format = "object") {
  if (!predictions.value.length) return null;

  // 이미지 정보 준비
  const imageInfo = {
    url: imageUrl.value,
    timestamp: new Date().toISOString(),
  };

  if (format === "object") {
    // 객체 형태로 반환
    const resultObject = {
      image: imageInfo,
      predictions: predictions.value.reduce((acc, pred) => {
        acc[pred.className] = {
          probability: pred.probability,
          percentage: (pred.probability * 100).toFixed(2) + "%",
        };
        return acc;
      }, {}),
      highestPrediction: {
        className: predictions.value[0].className,
        probability: predictions.value[0].probability,
        percentage: (predictions.value[0].probability * 100).toFixed(2) + "%",
      },
    };
    formattedResult.value = JSON.stringify(resultObject, null, 2);
    return resultObject;
  } else {
    // 배열 형태로 반환
    const resultArray = predictions.value.map((pred) => ({
      className: pred.className,
      probability: pred.probability,
      percentage: (pred.probability * 100).toFixed(2) + "%",
    }));
    formattedResult.value = JSON.stringify(resultArray, null, 2);
    return resultArray;
  }
}

// 외부에서 결과를 가져올 수 있는 함수
function getResults(format = "object") {
  return getFormattedResults(format);
}

function handleImageUpload(event) {
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
  imageUrl.value = URL.createObjectURL(file);
  formattedResult.value = null; // 새 이미지 업로드시 이전 결과 초기화
}

async function analyzeImage() {
  if (!model || !imagePreview.value) {
    error.value = "모델이 준비되지 않았습니다.";
    return;
  }

  try {
    const results = await model.predict(imagePreview.value);
    predictions.value = results.sort((a, b) => b.probability - a.probability);
    formattedResult.value = null; // 새 분석시 이전 포맷 결과 초기화
  } catch (err) {
    error.value = "이미지 분석 중 오류가 발생했습니다.";
    console.error("분석 오류:", err);
  }
}

async function initModel() {
  if (!window.tmImage) {
    error.value = "Teachable Machine 라이브러리가 아직 로드되지 않았습니다.";
    return;
  }

  try {
    const modelURL = `${modelPath.value}model.json`;
    const metadataURL = `${modelPath.value}metadata.json`;

    console.log("모델 로드 시도:", modelURL);
    model = await window.tmImage.load(modelURL, metadataURL);
    console.log("모델 로드 성공");
  } catch (err) {
    error.value = "모델을 불러오는 중 오류가 발생했습니다.";
    console.error("모델 로드 오류:", err);
  }
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

onMounted(async () => {
  try {
    await loadScript(
      "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"
    );
    await loadScript(
      "https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"
    );
    console.log("라이브러리 로드 완료");

    await initModel();
  } catch (err) {
    error.value = "초기화 중 오류가 발생했습니다.";
    console.error("초기화 오류:", err);
  }
});

// 외부에서 사용할 수 있도록 함수 노출
defineExpose({
  getResults,
});
</script>
<style>
.teachable-machine {
  color: white;
}
</style>
