<template>
  <div class="movie-detail-view">
    <div class="movie-container">
      <!-- 데이터가 없을 경우 에러 메시지 표시 -->
      <div v-if="error" class="error-message">
        <div class="siri-container">
          <div class="morph-layer layer-1"></div>
          <div class="morph-layer layer-2"></div>
          <div class="morph-layer layer-3"></div>
        </div>
        <h3>해당 ID에 대한 영화 데이터가 없습니다</h3>
      </div>
      <!-- 데이터가 있을 경우 영화 정보 및 리뷰 표시 -->
      <div v-else>
        <MovieInfo :movie="movieStore.movie" />
        <ReviewList />
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieInfo from "@/components/movieInfo.vue";
import ReviewList from "@/components/movieReviewList.vue";
import { onMounted, ref } from "vue"; // ref 추가
import { useMovieStore } from "@/stores/movieStore";
import { useRoute } from "vue-router"; // route 객체 가져오기

const movieStore = useMovieStore();
const route = useRoute(); // 현재 라우트 정보 가져오기

// 에러 상태 관리
const error = ref(false); // 에러 상태 초기화

onMounted(() => {
  const moviePk = route.params.moviePk; // URL에서 moviePk 추출
  movieStore
    .getMovie(moviePk)
    .then(() => {
      console.log("가져온 영화 데이터:", movieStore.movie);
      error.value = false; // 정상적으로 데이터를 가져온 경우 에러 상태 해제
    })
    .catch((err) => {
      console.error("API 호출 중 오류:", err);
      error.value = true; // 에러 발생 시 에러 상태 설정
    });
});
</script>

<style scoped>
@import "@/assets/styles/components/noDataCircle.css";

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
