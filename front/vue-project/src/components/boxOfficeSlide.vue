<template>
  <div class="coverflow-section">
    <h2 class="section-title">오늘 박스오피스 차트</h2>
    <div class="coverflow-wrapper">
      <button class="arrow left-arrow" @click="prevSlide">‹</button>
      <div class="coverflow-container">
        <div
          class="coverflow-item"
          v-for="(movie, index) in movies"
          :key="movie.movieCd"
          :class="{ active: index === currentIndex }"
          :style="getStyle(index)"
          @mouseover="hoverToCenter(index)"
          @click="openModal(movie)"
        >
          <div class="poster-container">
            <div class="rank-badge">{{ movie.rank }}</div>
            <img :src="movie.poster" alt="Movie Poster" />
          </div>
          <p class="title">{{ movie.movieNm }}</p>
        </div>
      </div>
      <button class="arrow right-arrow" @click="nextSlide">›</button>
    </div>

    <!-- Simple Modal -->
    <div v-if="selectedMovie" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close-btn" @click="closeModal">×</button>
        <img
          :src="selectedMovie.poster"
          :alt="selectedMovie.movieNm"
          class="modal-poster"
        />
        <div class="modal-info">
          <h3>{{ selectedMovie.movieNm }}</h3>
          <p class="movie-genre">{{ selectedMovie.genre }}</p>
          <p class="movie-open-date">{{ selectedMovie.openDt }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getBoxOfficeWithPosters } from "@/api/boxOfficeApi";

const movies = ref([]);
const currentIndex = ref(0);
const VISIBLE_ITEMS = 5;
const selectedMovie = ref(null);

const getStyle = (index) => {
  const totalMovies = movies.value.length;
  if (totalMovies === 0) return {};

  const positions = [];
  const center = Math.floor(VISIBLE_ITEMS / 2);

  // Calculate current position considering the circular nature
  let currentPosition = index - currentIndex.value;
  if (currentPosition < -center) currentPosition += totalMovies;
  if (currentPosition > center) currentPosition -= totalMovies;

  const absPosition = Math.abs(currentPosition);
  const zIndex = VISIBLE_ITEMS - absPosition;
  let translateX = currentPosition * 250;
  let scale = 1;

  // Apply transformations based on position
  if (absPosition === 0) {
    scale = 1.5;
  } else if (absPosition <= center) {
    scale = 1 - absPosition * 0.15;
  } else {
    scale = 0;
    translateX = currentPosition > 0 ? 1000 : -1000;
  }

  return {
    zIndex,
    transform: `translateX(${translateX}px) scale(${scale})`,
    opacity: absPosition <= center ? 1 : 0,
  };
};

const openModal = (movie) => {
  selectedMovie.value = movie;
};

const closeModal = () => {
  selectedMovie.value = null;
};

const hoverToCenter = (index) => {
  const center = Math.floor(VISIBLE_ITEMS / 2);
  const diff = index - currentIndex.value;

  if (Math.abs(diff) <= center) {
    currentIndex.value = index;
  }
};

const prevSlide = () => {
  const totalMovies = movies.value.length;
  currentIndex.value = (currentIndex.value - 1 + totalMovies) % totalMovies;
};

const nextSlide = () => {
  const totalMovies = movies.value.length;
  currentIndex.value = (currentIndex.value + 1) % totalMovies;
};

onMounted(async () => {
  movies.value = await getBoxOfficeWithPosters();
  currentIndex.value = 0;
});
</script>

<style scoped>
.coverflow-section {
  width: 100%;
  padding: 20px 0;
  background-color: rgba(0, 0, 0, 0.8);
  min-height: 600px;
}

.section-title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 30px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.coverflow-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 500px;
}

.coverflow-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  perspective: 1000px;
}

.coverflow-item {
  position: absolute;
  width: 150px;
  cursor: pointer;
  transition: all 0.5s ease;
}

.poster-container {
  position: relative;
  width: 150px;
  height: 220px;
}

.rank-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.1rem;
  font-weight: bold;
  z-index: 2;
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.coverflow-item img {
  width: 150px;
  height: 220px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.coverflow-item .title {
  text-align: center;
  margin-top: 10px;
  font-size: 0.9rem;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

.coverflow-item.active .title {
  opacity: 1;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  font-size: 2rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  user-select: none;
  z-index: 1000;
  transition: background 0.3s ease;
}

.arrow:hover {
  background: rgba(0, 0, 0, 0.7);
}

.left-arrow {
  left: 20px;
}

.right-arrow {
  right: 20px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
  position: relative;
  display: flex;
  gap: 20px;
}

.modal-close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 5px;
}

.modal-close-btn:hover {
  color: #333;
}

.modal-poster {
  width: 200px;
  height: auto;
  border-radius: 5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.modal-info {
  flex: 1;
  padding-top: 10px;
}

.modal-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.5rem;
  color: #333;
}

.movie-genre {
  color: #666;
  margin: 5px 0;
}

.movie-open-date {
  color: #888;
  margin: 5px 0;
}

@media (max-width: 600px) {
  .modal-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .modal-poster {
    width: 180px;
  }
}
</style>
