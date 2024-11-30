<!-- src/components/BoxOffice.vue -->
<template>
  <div class="coverflow-section">
    <h2 class="section-title">오늘의 박스오피스</h2>
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
            <img 
              :src="movie.tmdbDetails?.posterPath || 'https://via.placeholder.com/150'" 
              :alt="movie.movieNm" 
              class="poster-image"
            />
          </div>
          <p class="title">{{ movie.movieNm }}</p>
        </div>
      </div>
      <button class="arrow right-arrow" @click="nextSlide">›</button>
    </div>

    <!-- 모달 -->
    <div v-if="selectedMovie" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 class="movie-title">{{ selectedMovie.movieNm }}</h3>
          <div class="modal-buttons">
            <button class="detail-btn" @click="goToMovieDetail(selectedMovie)">
              상세정보
            </button>
            <button class="close-btn" @click="closeModal">닫기</button>
          </div>
        </div>
        <div class="modal-body">
          <div class="modal-poster-section">
            <img
              :src="selectedMovie.tmdbDetails?.posterPath"
              :alt="selectedMovie.movieNm"
              class="modal-poster"
            />
          </div>
          <div class="modal-info-section">
            <div class="info-row">
              <p class="release-date">개봉일: {{ formatDate(selectedMovie.tmdbDetails?.releaseDate) }}</p>
            </div>
            <div class="genre-badges">
              <span 
                v-for="genre in selectedMovie.tmdbDetails?.genres.split(', ')" 
                :key="genre" 
                class="genre-badge"
              >
                {{ genre }}
              </span>
            </div>
            <div class="overview-section">
              <h4>줄거리</h4>
              <p 
                class="overview" 
                :class="{ 'expanded': isExpanded }"
              >
                {{ selectedMovie.tmdbDetails?.overview || '줄거리 정보가 없습니다.' }}
              </p>
              <button 
                v-if="hasLongOverview" 
                class="toggle-btn"
                @click="toggleOverview"
              >
                {{ isExpanded ? '접기' : '더보기' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from 'vue-router';
import { getBoxOfficeWithDetails } from "@/api/boxOfficeApi";
import { useMovieStore } from "@/stores/movieStore";

const router = useRouter();
const movieStore = useMovieStore();

const movies = ref([]);
const currentIndex = ref(0);
const VISIBLE_ITEMS = 5;
const selectedMovie = ref(null);
const isExpanded = ref(false);
const OVERVIEW_MAX_LENGTH = 150;

const hasLongOverview = computed(() => {
  return selectedMovie.value?.tmdbDetails?.overview?.length > OVERVIEW_MAX_LENGTH;
});

const formatDate = (dateString) => {
  if (!dateString) return '날짜 정보 없음';
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};

const getStyle = (index) => {
  const totalMovies = movies.value.length;
  if (totalMovies === 0) return {};

  const center = Math.floor(VISIBLE_ITEMS / 2);
  let currentPosition = index - currentIndex.value;
  
  if (currentPosition < -center) currentPosition += totalMovies;
  if (currentPosition > center) currentPosition -= totalMovies;

  const absPosition = Math.abs(currentPosition);
  const zIndex = VISIBLE_ITEMS - absPosition;
  let translateX = currentPosition * 250;
  let scale = 1;

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
  isExpanded.value = false;
  document.body.style.overflow = 'hidden';
};

const closeModal = () => {
  selectedMovie.value = null;
  document.body.style.overflow = 'auto';
};

const toggleOverview = () => {
  isExpanded.value = !isExpanded.value;
};

const goToMovieDetail = async (movie) => {
  try {
    console.log('전달받은 영화 데이터:', movie); // 디버깅용

    // TMDB 영화 정보를 단순화해서 전달 (null 체크 추가)
    const movieData = {
      id: movie.tmdbDetails.tmdbId,
      tmdb_id: movie.tmdbDetails.tmdbId,
      title: movie.movieNm,
      original_title: movie.tmdbDetails.originalTitle || movie.movieNm, // 영어 제목이 없으면 한글 제목 사용
      description: movie.tmdbDetails.overview || '',
      poster_path: movie.tmdbDetails.posterPath || '',
      release_date: movie.tmdbDetails.releaseDate || '',
      vote_average: movie.tmdbDetails.voteAverage || 0,
      runtime: movie.tmdbDetails.runtime?.toString() || '0',
      popularity: 0,
      genres: Array.isArray(movie.tmdbDetails.genres) 
        ? movie.tmdbDetails.genres 
        : (movie.tmdbDetails.genres || '').split(', ').filter(Boolean),
      cast: Array.isArray(movie.tmdbDetails.cast) 
        ? movie.tmdbDetails.cast.map(actor => ({
            name: actor.name,
            profile_path: actor.profilePath || '',
            character: actor.character || ''
          }))
        : [],
      director: typeof movie.tmdbDetails.director === 'string'
        ? [{ name: movie.tmdbDetails.director, profile_path: '' }]
        : []
    };

    console.log('가공된 영화 데이터:', movieData); // 디버깅용

    // createOrGetMovie 호출 후 바로 라우팅
    const savedMovie = await movieStore.createOrGetMovie(movieData);
    console.log('저장된 영화 데이터:', savedMovie); // 디버깅용
    
    closeModal();
    await router.push(`/movies/${savedMovie.id}`);
  } catch (error) {
    console.error('영화 상세 페이지 이동 중 오류:', error);
    console.error('문제가 발생한 영화 데이터:', movie); // 디버깅용
    alert('영화 정보를 불러오는데 실패했습니다.');
  }
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
  movies.value = await getBoxOfficeWithDetails();
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

.poster-image {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  object-fit: cover;
}

.title {
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

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background-color: #1a1a1a;
  color: white;
  border-radius: 15px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  position: relative;
  overflow: hidden;
}

.modal-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
}

.movie-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0;
  color: white;
}

.modal-buttons {
  display: flex;
  gap: 10px;
}

.close-btn, .detail-btn {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.close-btn {
  background-color: #333;
  color: white;
}

.detail-btn {
  background-color: #0078ff;
  color: white;
}

.close-btn:hover, .detail-btn:hover {
  opacity: 0.8;
}

.modal-body {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  padding: 20px;
}

.modal-poster-section {
  width: 100%;
}

.modal-poster {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
}

.modal-info-section {
  color: white;
}

.info-row {
  margin-bottom: 15px;
}

.release-date {
  color: #888;
  margin: 0;
}

.genre-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 15px 0;
}

.genre-badge {
  background-color: #333;
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
}

.overview-section {
  margin-top: 20px;
}

.overview-section h4 {
  color: white;
  margin-bottom: 10px;
  font-size: 1.2rem;
}

.overview {
  color: #ccc;
  line-height: 1.6;
  max-height: 80px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.overview.expanded {
  max-height: 1000px;
}

.toggle-btn {
  background: none;
  border: none;
  color: #0078ff;
  cursor: pointer;
  padding: 5px 0;
  margin-top: 10px;
  font-size: 0.9rem;
}

.toggle-btn:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .modal-body {
    grid-template-columns: 1fr;
  }

  .modal-poster-section {
    max-width: 300px;
    margin: 0 auto;
  }

  .modal-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .modal-content {
    width: 95%;
    margin: 20px;
    max-height: calc(100vh - 40px);
  }

  .movie-title {
    font-size: 1.5rem;
  }
}
</style>