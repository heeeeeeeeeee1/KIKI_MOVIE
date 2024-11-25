<template>
  <div class="roulette-container">
    <Roulette
      ref="wheel"
      :key="rouletteKey"
      :items="items"
      size="500"
      base-background="#FFD700"
      base-size=80
      centere-indicator
      indicator-position="top"
      display-shadow
      :display-border="false"
      base-display
      base-display-indicator
      base-display-shadow
      easing="bounce"
      @wheel-start="wheelStartedCallback"
      @wheel-end="wheelEndedCallback"
      @click="launchWheel"
    >
      <template #baseContent>
        <div class="go-btn" >GO!</div>
      </template>
    </Roulette>

    <div class="button-container">
      <button @click="loadRandomMovies">영화 다시 섞기</button>
    </div>

    <p v-if="error" class="error-message">Error: {{ error }}</p>
    <p v-if="isLoading" class="loading-message">Loading...</p>

    <!-- 모달 -->
    <div v-if="selectedMovie" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2>{{ selectedMovie.name }}</h2>
        <img :src="'https://image.tmdb.org/t/p/w500' + selectedMovie.poster_path" :alt="selectedMovie.name" />
        <p>{{ selectedMovie.overview }}</p>
        <button @click="closeModal">닫기</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useTmdb } from "@/api/tmdb";
import { Roulette } from "vue3-roulette";

export default {
  name: "RouletteView",
  components: {
    Roulette,
  },
  setup() {
    const rouletteKey = ref(0); // 룰렛의 고유 키
    const items = ref([]); // 룰렛의 영화 아이템
    const wheel = ref(null); // 룰렛 컴포넌트 참조
    const selectedMovie = ref(null); // 선택된 영화 데이터
    const { movies, isLoading, error, fetchPopularMovies } = useTmdb(); // TMDB API 호출 함수 및 상태

    // 영화 데이터 로드
  const loadRandomMovies = async () => {
    const randomPage = Math.floor(Math.random() * 500) + 1;
    await fetchPopularMovies(randomPage);
    
    // 데이터 로드 직전에 wheel-item 스타일 설정
    setTimeout(() => {
      const wheelItems = document.querySelectorAll('.wheel-item');
      wheelItems.forEach(item => {
        item.style.backgroundColor = 'black';
      });
    }, 0);
    
    items.value = movies.value.slice(0, 8).map((movie, index) => ({
      id: movie.id,
      name: movie.title,
      poster_path: movie.poster_path,
      overview: movie.overview,
      htmlContent: `
        <div class="my-wheel">
          <img src="https://image.tmdb.org/t/p/w200${movie.poster_path}" alt="${movie.title}" class="roulette-poster"/>
        </div>
      `
    }));
  };

    // 룰렛 시작
    const launchWheel = () => {
      rouletteKey.value += 1; // 새로운 키로 초기화
      setTimeout(() => wheel.value.launchWheel(), 0);
    };

    // 룰렛 시작 콜백
    const wheelStartedCallback = () => {
      console.log("Wheel started!");
    };

    // 룰렛 종료 콜백
    const wheelEndedCallback = (event) => {
      selectedMovie.value = items.value.find((item) => item.id === event.id); // 선택된 영화 찾기
      console.log("Selected item:", selectedMovie.value);
    };

    // 모달 닫기
    const closeModal = () => {
      selectedMovie.value = null;
    };

    // 컴포넌트 마운트 시 영화 데이터 로드
    onMounted(() => {
      loadRandomMovies();
    });

    return {
      rouletteKey,
      items,
      wheel,
      selectedMovie,
      isLoading,
      error,
      loadRandomMovies,
      launchWheel,
      wheelStartedCallback,
      wheelEndedCallback,
      closeModal,
    };
  },
};
</script>

<style scoped>

.roulette-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* 화면 중앙 정렬 */
  text-align: center;
}

.wheel .wheel-item:nth-child(odd) {
  background: linear-gradient(to right, #000000, #0a0a0a);
}

.wheel .wheel-item:nth-child(even) {
  background: linear-gradient(to right, #000000, #0a0a0a); /* 빨간색 */
}

.wheel .wheel-item {
  font-weight: bold;
  color: white;
  text-shadow: 0px 5px 10px black;
}

.button-container {
  margin-top: 20px; /* 버튼과 룰렛 간격 */
}

button {
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.loading-message {
  color: #007bff;
  margin-top: 10px;
}

.go-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: black; /* GO! 버튼 글씨 색상: 검정 */
  font-size:25px; /* 글씨 크기 줄임 */
  font-weight: bold;
  border: none;
  cursor: pointer;
}



.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  text-align: center;
}

.modal-content img {
  max-width: 100%;
  height: auto;
  margin-bottom: 20px;
}

.modal-content button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
}

.modal-content button:hover {
  background-color: #0056b3;
}

.roulette-poster {
  width: 200px; /* 영화 포스터 크기 조정 */
  height: auto; /* 비율 유지 */
}

.wheel-container-indicator::before {
  border-top: 20px solid red;
  transform: rotate(45deg); 
}
</style>
