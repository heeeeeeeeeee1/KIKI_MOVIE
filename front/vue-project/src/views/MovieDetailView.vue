<template>
  <div class="movie-detail-view">
    <main class="movie-container">
      <MovieInfo :movie="movieStore.movie" />
      <ReviewList />
    </main>
  </div>
</template>

<script setup>
import MovieInfo from "@/components/movieInfo.vue";
import ReviewList from "@/components/movieReviewList.vue";
import { onMounted } from "vue";
import { useMovieStore } from "@/stores/movieStore";

const movieStore = useMovieStore();

onMounted(() => {
  const moviePk = 98; // 테스트용 영화 PK
  movieStore
    .getMovie(moviePk) // 영화 정보 호출
    .then(() => {
      console.log("가져온 영화 데이터:", movieStore.movie);
    })
    .catch((error) => {
      console.error("API 호출 중 오류:", error);
    });
});
</script>

<style scoped>
.movie-detail-view {
  width: 100%;
  display: flex;
  justify-content: center;
}
.movie-container {
  width: 60%;
  margin: auto 0;
  background-color: inherit;
  color: white;
}
</style>
