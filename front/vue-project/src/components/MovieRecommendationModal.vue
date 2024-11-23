<!-- MovieRecommendationModal -->
<template>
  <div class="modal-overlay" v-if="isVisible">
    <div class="modal-content">
      <h2>추천 영화</h2>
      <div v-if="movies.length" class="movies">
        <div v-for="movie in movies" :key="movie.id" class="movie-card">
          <img
            :src="'https://image.tmdb.org/t/p/w200' + movie.poster_path"
            :alt="movie.title"
          />
          <p>{{ movie.title }}</p>
        </div>
      </div>
      <p v-else>추천 영화를 불러오는 중...</p>
      <button @click="closeModal">닫기</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isVisible: Boolean, // 모달 보이기 여부
    movies: Array, // 추천 영화 리스트
  },
  emits: ["close"],
  methods: {
    closeModal() {
      this.$emit("close"); // 모달 닫기
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 80%;
  max-width: 600px;
}
.movies {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}
.movie-card {
  text-align: center;
  width: 100px;
}
.movie-card img {
  width: 100%;
  border-radius: 8px;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
