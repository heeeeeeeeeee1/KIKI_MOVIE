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
          <div v-if="actorProfile" class="actor-profile">
            <img
              :src="actorProfile.profile_path ? 'https://image.tmdb.org/t/p/w500' + actorProfile.profile_path : '/default-profile.png'"
              alt="Actor Profile"
              class="actor-photo"
            />
          </div>
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
import { getMoviesByActor, getActorDetails } from "../api/tmdb";

const error = ref(null);
const imageUrl = ref(null);
const imagePreview = ref(null);
const predictions = ref([]);
const topPrediction = ref(null);
const movies = ref([]);
const actorProfile = ref(null); // 배우 프로필 정보 저장

let model = null;
const modelPath = ref("/models/my-model/");

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
    const reader = new FileReader();
    reader.onload = (e) => (imageUrl.value = e.target.result);
    reader.readAsDataURL(file); // 이미지를 그대로 로드하여 표시
  } catch (err) {
    error.value = "이미지 로드 중 오류가 발생했습니다: " + err.message;
    console.error("이미지 로드 오류:", err);
  }
};

const analyzeImage = async () => {
  if (!model || !imagePreview.value) {
    error.value = "모델이 준비되지 않았습니다.";
    return;
  }

  try {
    const results = await model.predict(imagePreview.value);
    predictions.value = results.sort((a, b) => b.probability - a.probability);

    if (predictions.value.length > 0) {
      topPrediction.value = predictions.value[0];
      const actorId = getActorId(topPrediction.value?.className);

      if (actorId) {
        actorProfile.value = await getActorDetails(actorId);
        movies.value = await getMoviesByActor(actorId);
      }
    }
  } catch (err) {
    error.value = "이미지 분석 중 오류가 발생했습니다.";
    console.error(err);
  }
};

const initModel = async () => {
  if (!window.tmImage) {
    error.value = "Teachable Machine 라이브러리가 아직 로드되지 않았습니다.";
    return;
  }

  try {
    const modelURL = `${modelPath.value}model.json`;
    const metadataURL = `${modelPath.value}metadata.json`;

    model = await window.tmImage.load(modelURL, metadataURL);
  } catch (err) {
    model = null;
    error.value = "모델 로드 중 오류가 발생했습니다.";
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
    console.error(err);
  }
});

onUnmounted(() => {
  if (model && typeof model.dispose === "function") {
    model.dispose();
  }
});
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

.img-container,
.actor-profile {
  width: 100%;
  min-height: 500px;
}

.img-container img,
.actor-profile img {
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
