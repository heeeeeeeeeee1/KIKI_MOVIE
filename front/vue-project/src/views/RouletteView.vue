<template>
  <div class="roulette-container">
    <h2 class="roulette-title">오늘 볼 영화는?</h2>
    <section class="section-roulette">
      <div class="roulette-wrapper">
        <Roulette
          ref="wheel"
          :key="rouletteKey"
          :items="items"
          size="500"
          base-background="#FFD700"
          base-size="80"
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
            <div class="go-btn">GO!</div>
          </template>
        </Roulette>
      </div>
    </section>
    <section class="section-button">
      <button @click="loadRandomMovies">영화 다시 고르기</button>
    </section>
    <section class="section-message">
      <p v-if="error" class="error-message">Error: {{ error }}</p>
      <p v-if="isLoading" class="loading-message">Loading...</p>
    </section>
    <!-- 모달 -->
    <section v-if="selectedMovie" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2 class="modal-title">{{ selectedMovie.name }}</h2>
        <div class="modal-genres" v-if="selectedMovie.genres?.length">
          <span
            v-for="genre in selectedMovie.genres"
            :key="genre"
            class="genre-tag"
          >
            {{ genre }}
          </span>
        </div>
        <div class="modal-imgcontainer">
          <div
            class="img-wrapper"
            :class="{ 'adult-content': selectedMovie.adult }"
          >
            <img
              :src="
                'https://image.tmdb.org/t/p/w500' + selectedMovie.poster_path
              "
              :alt="selectedMovie.name"
              :class="{ blurred: selectedMovie.adult && !showAdultImage }"
            />
            <div
              v-if="selectedMovie.adult && !showAdultImage"
              class="adult-warning"
            >
              <p>
                🔞 <br />유해한 콘텐츠 <br />
                가능성이 높아요
              </p>
              <button class="show-image-btn" @click="showAdultImage = true">
                포스터 이미지 보기
              </button>
            </div>
          </div>
        </div>
        <div class="modal-overview-container">
          <p
            v-if="selectedMovie.overview"
            class="modal-overview"
            :class="{ expanded: isExpanded }"
          >
            {{ selectedMovie.overview }}
          </p>
          <p v-else class="modal-overview no-overview">
            설명은 비록 없지만 당신이 상상력을 더할 수 있어요
          </p>
          <button
            v-if="selectedMovie.overview && isOverflowing"
            class="overview-toggle-btn"
            @click="toggleOverview"
          >
            {{ isExpanded ? "접기" : "더보기" }}
          </button>
        </div>
        <div class="modal-buttons">
          <button class="detail-btn" @click="goToMovieDetail">상세 정보 보기</button>
          <button class="modal-close-btn" @click="closeModal">닫기</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useTmdb } from "@/api/tmdb";
import { Roulette } from "vue3-roulette";
import { useRouter } from 'vue-router';
import { useMovieStore } from '@/stores/movieStore';

export default {
  name: "RouletteView",
  components: {
    Roulette,
  },
  setup() {
    const router = useRouter();
    const movieStore = useMovieStore();
    const rouletteKey = ref(0);
    const items = ref([]);
    const wheel = ref(null);
    const selectedMovie = ref(null);
    const isExpanded = ref(false);
    const isOverflowing = ref(false);
    const showAdultImage = ref(false);
    const { movies, isLoading, error, fetchPopularMovies } = useTmdb();

    const checkOverflow = () => {
      if (selectedMovie.value && selectedMovie.value.overview) {
        const overviewElement = document.querySelector(".modal-overview");
        if (overviewElement) {
          isOverflowing.value =
            overviewElement.scrollHeight > overviewElement.clientHeight;
        }
      }
    };

    const toggleOverview = () => {
      isExpanded.value = !isExpanded.value;
    };

    const loadRandomMovies = async () => {
      const randomPage = Math.floor(Math.random() * 500) + 1;
      await fetchPopularMovies(randomPage);

      setTimeout(() => {
        const wheelItems = document.querySelectorAll(".wheel-item");
        wheelItems.forEach((item) => {
          item.style.backgroundColor = "black";
        });
      }, 0);

      items.value = movies.value.slice(0, 8).map((movie) => ({
        ...movie,
        name: movie.title,
        htmlContent: `
          <div class="my-wheel">
            <img src="https://image.tmdb.org/t/p/w200${movie.poster_path}" alt="${movie.title}" class="roulette-poster"/>
          </div>
        `,
      }));
    };

    const launchWheel = () => {
      rouletteKey.value += 1;
      setTimeout(() => wheel.value.launchWheel(), 0);
    };

    const wheelStartedCallback = () => {
      console.log("Wheel started!");
    };

    const wheelEndedCallback = (event) => {
      selectedMovie.value = items.value.find((item) => item.id === event.id);
      isExpanded.value = false;
      showAdultImage.value = false;
      setTimeout(checkOverflow, 0);
    };

    const goToMovieDetail = async (movie) => {
      if (!movie) return;

      try {
        // TMDB 영화 데이터를 Django에 저장 또는 가져오기
        const savedMovie = await movieStore.createOrGetMovie(movie);
        if (savedMovie && savedMovie.id) {
          router.push({ name: "MovieDetailView", params: { moviePk: savedMovie.id } });
        } else {
          console.error("영화 저장 또는 가져오기 실패");
        }
      } catch (err) {
        console.error("영화 상세 페이지 이동 실패:", err);
      }
    };


    const closeModal = () => {
      selectedMovie.value = null;
      isExpanded.value = false;
      showAdultImage.value = false;
    };

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
      isExpanded,
      isOverflowing,
      showAdultImage,
      loadRandomMovies,
      launchWheel,
      wheelStartedCallback,
      wheelEndedCallback,
      closeModal,
      toggleOverview,
      goToMovieDetail,
    };
  },
};
</script>

<style scoped>
.roulette-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  text-align: center;
  padding-top: 3rem;
}

.roulette-container > * {
  width: 80%;
}

.roulette-title {
  font-weight: 550;
  margin-bottom: 2rem;
}

.section-roulette {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 2rem;
}

.roulette-wrapper {
  width: 532px;
  height: 532px;
  background-color: var(--dark-gray);
  padding: 1rem;
  border-radius: 50%;
}

.section-button {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.section-button button {
  background-color: var(--light-blue);
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.section-button button:hover {
  background-color: var(--dark-blue);
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--dark-gray);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 1rem;
  padding: 2rem;
  position: relative;
  color: white;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: white;
}

.modal-imgcontainer {
  width: 100%;
  margin-bottom: 1.5rem;
}

.img-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.img-wrapper img {
  width: 100%;
  max-width: 300px;
  height: auto;
  border-radius: 0.5rem;
  transition: filter 0.3s ease;
}

.img-wrapper img.blurred {
  filter: blur(20px);
}

.adult-warning {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  background-color: rgba(0, 0, 0, 0.8);
  padding: 1rem;
  border-radius: 0.5rem;
  z-index: 1;
}

.adult-warning p {
  line-height: 1.75rem;
}

.adult-warning p {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.show-image-btn {
  background-color: var(--light-blue);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.show-image-btn:hover {
  background-color: var(--hover-blue);
}

.adult-content::before {
  content: "🔞";
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  z-index: 2;
}

.modal-overview-container {
  position: relative;
  margin-bottom: 2rem;
}

.modal-overview {
  font-size: 1rem;
  line-height: 1.6;
  color: #e0e0e0;
  text-align: left;
  max-height: 4.8em;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.modal-overview.expanded {
  max-height: none;
}

.no-overview {
  color: #888;
  font-style: italic;
  text-align: center;
}

.overview-toggle-btn {
  background: none;
  border: none;
  color: var(--light-blue);
  cursor: pointer;
  padding: 0.5rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.overview-toggle-btn:hover {
  color: var(--hover-blue);
}

.modal-overview:not(.expanded):not(.no-overview)::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2em;
  background: linear-gradient(transparent, var(--dark-gray));
  pointer-events: none;
  opacity: 1;
  transition: opacity 0.3s ease;
}

.modal-overview.expanded::after {
  opacity: 0;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.detail-btn, .modal-close-btn {
  background-color: var(--light-blue);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.detail-btn:hover, .modal-close-btn:hover {
  background-color: var(--hover-blue);
}

/* 스크롤바 스타일링 */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: var(--dark-gray);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: var(--light-blue);
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: var(--hover-blue);
}

.error-message {
  color: #ff4444;
  font-size: 1rem;
  margin-top: 1rem;
}

.loading-message {
  color: var(--light-blue);
  font-size: 1rem;
  margin-top: 1rem;
}

.roulette-poster {
  width: 200px;
  height: auto;
  border-radius: 0.25rem;
}

.modal-genres {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.genre-tag {
  background-color: var(--light-blue);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  white-space: nowrap;
}
</style>