<!-- PredictActor.vue -->
<template>
  <div class="predict-actor">
    <h1>닮은꼴 배우 찾기</h1>
    
    <div class="upload-section">
      <label for="file-upload" class="custom-file-upload">
        이미지 선택
        <input 
          id="file-upload" 
          type="file" 
          @change="handleFileUpload"
          accept="image/*"
        />
      </label>
      
      <div v-if="imagePreview" class="preview-container">
        <img :src="imagePreview" alt="Preview" class="image-preview" />
      </div>
      
      <button 
        @click="predictActor" 
        :disabled="!imageFile"
        class="predict-button"
      >
        닮은꼴 찾기
      </button>
    </div>

    <div v-if="loading" class="loading">
      분석 중...
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="actor" class="result-container">
      <h2>추천 배우: {{ actor }}</h2>
      <div class="movie-list">
        <h3>출연 영화:</h3>
        <div class="movie-grid">
          <div 
            v-for="movie in movies" 
            :key="movie.id"
            class="movie-card"
            @click="goToMovieDetail(movie.id)"
          >
            <img 
              :src="movie.poster_path || '/placeholder-poster.png'" 
              :alt="movie.title" 
              class="movie-poster"
            />
            <div class="movie-info">
              <h4>{{ movie.title }}</h4>
              <p>{{ formatDate(movie.release_date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from 'vue-router';

export default {
  name: "PredictActor",
  setup() {
    const router = useRouter();
    const imageFile = ref(null);
    const imagePreview = ref(null);
    const actor = ref(null);
    const movies = ref([]);
    const error = ref(null);
    const loading = ref(false);

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        imageFile.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          imagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    const goToMovieDetail = (movieId) => {
      router.push(`/movie/${movieId}`);
    };

    const predictActor = async () => {
      if (!imageFile.value) {
        error.value = "이미지를 업로드하세요.";
        return;
      }

      loading.value = true;
      error.value = null;

      const formData = new FormData();
      formData.append("image", imageFile.value);

      try {
        const response = await fetch("http://127.0.0.1:8000/predictions/predict/", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
          error.value = data.error;
        } else {
          actor.value = data.actor;
          movies.value = data.movies;
        }
      } catch (err) {
        console.error("Error:", err);
        error.value = `서버 통신 오류: ${err.message}`;
      } finally {
        loading.value = false;
      }
    };

    return {
      imageFile,
      imagePreview,
      actor,
      movies,
      error,
      loading,
      handleFileUpload,
      predictActor,
      formatDate,
      goToMovieDetail
    };
  },
};
</script>

<style scoped>
.predict-actor {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.upload-section {
  margin: 20px 0;
  text-align: center;
}

.custom-file-upload {
  display: inline-block;
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin: 10px;
}

.custom-file-upload input[type="file"] {
  display: none;
}

.preview-container {
  margin: 20px 0;
}

.image-preview {
  max-width: 300px;
  max-height: 300px;
  object-fit: contain;
}

.predict-button {
  padding: 10px 20px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.predict-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  margin: 20px 0;
  font-size: 18px;
}

.error {
  color: #f44336;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #f44336;
  border-radius: 5px;
}

.result-container {
  margin-top: 30px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.2s;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.movie-info {
  padding: 10px;
}

.movie-info h4 {
  margin: 0;
  font-size: 16px;
}

.movie-info p {
  margin: 5px 0 0;
  color: #666;
  font-size: 14px;
}
</style>