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
  const moviePk = 98;
  movieStore
    .getMovie(moviePk)
    .then(() => {
      console.log("가져온 영화 데이터:", movieStore.movie);
      // console.log 결과 : "/yemF0xxGU56Pf3JXxVr4C6kuKng.jpg"
      console.log(movieStore.movie.poster_path)
      // console.log(movieStore.movie.actors.map(actor => actor.name).join(", "));
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
