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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 80vh;
  font-size: 1.5rem;
  text-align: center;
  margin: 2rem 0;
}
.error-message h3 {
  font-size: 1.6rem;
  color: white;
  font-weight: bold;
  margin-top: 5rem;
}

.siri-container {
    position: relative;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.7));
    overflow: hidden;
    z-index: 1;
    box-shadow: 0 0 50px rgba(255, 255, 255, 0.5);
  }

  .morph-layer {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: conic-gradient(
      from 0deg,
      rgba(255, 0, 0, 0.3),
      rgba(0, 255, 0, 0.3),
      rgba(0, 0, 255, 0.3),
      rgba(255, 0, 255, 0.3),
      rgba(255, 255, 0, 0.3),
      rgba(255, 0, 0, 0.3)
    );
    animation: rotate-gradient 10s linear infinite, morph-shape 6s ease-in-out infinite alternate;
    filter: blur(60px);
    z-index: -1; /* Siri 원 뒤로 이동 */
  }

  /* 레이어별 크기 */
  .layer-1 {
    width: 300%;
    height: 300%;
    animation-duration: 8s;
    filter: blur(80px); /* 가장 넓고 부드럽게 퍼지는 그림자 */
  }

  .layer-2 {
    width: 250%;
    height: 250%;
    animation-duration: 6s;
    filter: blur(60px);
  }

  .layer-3 {
    width: 200%;
    height: 200%;
    animation-duration: 4s;
    filter: blur(40px);
  }

  @keyframes rotate-gradient {
    0% {
      transform: translate(-50%, -50%) rotate(0deg);
    }
    100% {
      transform: translate(-50%, -50%) rotate(360deg);
    }
  }

  @keyframes morph-shape {
    0% {
      clip-path: circle(50%);
    }
    50% {
      clip-path: ellipse(60% 50%);
    }
    100% {
      clip-path: circle(50%);
    }
  }
</style>
