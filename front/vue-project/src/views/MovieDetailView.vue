<template>
  <div class="movie-detail-view">
    <div class="movie-container">
      <!-- 데이터가 없을 경우 에러 메시지 표시 -->
      <div v-if="error" class="error-message">
        <div class="ghost-circle">
          <h3>해당 ID에 대한<br>영화 정보가 없습니다</h3>
        </div>
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
.error-message {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  font-size: 1.5rem;
  text-align: center;
  margin: 2rem 0;
}

.ghost-circle {
    position: relative;
    width: 15rem;
    height: 15rem;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0));
    animation: ghost-float 3s ease-in-out infinite;
    box-shadow: 0 0 20px 10px rgba(255, 255, 255, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }
.ghost-circle h3 {
  font-size: 1.6rem;
  color: black;
  font-weight: bold;
}

.ghost-circle::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0));
  border-radius: 50%;
  animation: ghost-shadow 4s ease-in-out infinite;
}

@keyframes ghost-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes ghost-shadow {
  0% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(1.1);
  }
  100% {
    transform: rotate(360deg) scale(1);
  }
}
</style>
