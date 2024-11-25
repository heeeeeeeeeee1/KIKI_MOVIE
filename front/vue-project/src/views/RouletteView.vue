<template>
  <div class="roulette-container">
    <Roulette
      ref="wheel"
      :key="rouletteKey"
      :items="items"
      centered-indicator
      indicator-position="top"
      display-shadow
      display-border
      base-display
      base-display-indicator
      base-background="#dedede"
      base-display-shadow
      easing="bounce"
      @wheel-start="wheelStartedCallback"
      @wheel-end="wheelEndedCallback"
      @click="launchWheel"
    >
      <template #baseContent>
        <div class="go-btn">GO!</div>
      </template>
    </Roulette>

    <div class="button-container">
      <button @click="resetWheel">Reset</button>
      <button @click="hardResetWheel">Hard Reset</button>
      <button @click="loadRandomMovies">오늘의 추천 영화</button>
    </div>
    <p v-if="error" class="error-message">Error: {{ error }}</p>
    <p v-if="isLoading" class="loading-message">Loading...</p>
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
    const rouletteKey = ref(0);
    const items = ref([]);
    const wheel = ref(null);
    const { movies, isLoading, error, fetchPopularMovies } = useTmdb();

    const loadRandomMovies = async () => {
      const randomPage = Math.floor(Math.random() * 500) + 1;
      await fetchPopularMovies(randomPage);
      items.value = movies.value.slice(0, 8).map((movie) => ({
        id: movie.id,
        name: movie.title,
        htmlContent: `
          <div style="text-align: center;">
            <img src="https://image.tmdb.org/t/p/w200${movie.poster_path}" alt="${movie.title}" style="width: 100px; height: auto;"/>
          </div>
        `,
        textColor: "#000",
        background: "#fff",
      }));
    };

    const launchWheel = () => {
      rouletteKey.value += 1;
      setTimeout(() => wheel.value.launchWheel(), 0);
    };

    const resetWheel = () => {
      wheel.value.reset();
    };

    const hardResetWheel = () => {
      rouletteKey.value += 1;
    };

    const wheelStartedCallback = () => {
      console.log("Wheel started!");
    };

    const wheelEndedCallback = (event) => {
      console.log("Selected item:", event);
    };

    onMounted(() => {
      loadRandomMovies();
    });

    return {
      rouletteKey,
      items,
      wheel,
      isLoading,
      error,
      loadRandomMovies,
      launchWheel,
      resetWheel,
      hardResetWheel,
      wheelStartedCallback,
      wheelEndedCallback,
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
  height: 100vh; /* 화면 중앙 정렬을 위해 */
  text-align: center;
}

.button-container {
  margin-top: 20px; /* 버튼과 룰렛 사이 여백 */
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
  background-color: var(--dark-blue); /* 수정: 버튼 배경색을 초록색으로 변경 */
  color: white; /* 텍스트 색상은 흰색 유지 */
  padding: 10px 10px; /* 수정: 내부 여백을 줄여 버튼 크기 축소 */
  font-size: 12px; /* 수정: 텍스트 크기를 12px로 축소 */
  font-weight: bold;
  border: none;
  border-radius: 50%; /* 버튼을 원형으로 유지 */
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.go-btn:hover {
  background-color: #218838; /* 수정: 호버 시 더 진한 초록색으로 변경 */
}
</style>
