<!-- ProfileReaction.vue -->
<template>
  <div class="profile-reaction">
    <button 
      :class="{ active: activeList === 'watched' }"
      @click="switchTo('watched')"
    >
      봤어요
    </button>
    <button
      :class="{ active: activeList === 'wishlist' }"
      @click="switchTo('wishlist')"
    >
      보고싶어요
    </button>
  </div>

  <!-- 봤어요  -->
  <div class="my-movie-container">
    <div class="watched-info" v-if="activeList === 'watched'">
      <div v-if="!watchedMovies.length" class="empty-list">
        아직 감상한 영화가 없습니다.
      </div>
      <div
        v-else
        v-for="(review, index) in watchedMovies"
        :key="review.id"
        class="watched-items"
        :style="getItemDelay(index)"
        @click="goToReviewDetail(review.movie.id, review.id)"
      >
        <div class="left-info">
          <div class="poster-container">
            <img :src="tmdb_base_url + review.movie.poster_path" alt="movie-poster" />
          </div>
        </div>
        <div class="right-info">
          <div class="movie-info">
            <h4>{{ review.movie.title }}</h4>
            <div class="genre-badges">
              <span 
                v-for="genre in review.movie_genres" 
                :key="genre" 
                class="genre-badge"
                :style="{ backgroundColor: getGenreColor(genre) }"
              >
                {{ genre }}
              </span>
            </div>
          </div>
          <div class="rating">
            <span 
              v-for="n in 5" 
              :key="n"
              class="star"
              :class="{ filled: n <= review.score }"
            >★</span>
          </div>
          <p class="review-content">{{ review.content }}</p>
          <div class="interaction-info">
            <span>댓글 {{ review.comment_count }}</span>
            <span>좋아요 {{ review.like_count }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 보고싶어요 -->
    <div class="my-movie-container wish-info">
      <div v-if="activeList === 'wishlist'" class="wish-list">
        <div v-if="!wishlistMovies.length" class="empty-list">
          아직 보고 싶은 영화가 없습니다.
        </div>
        <div 
          v-else
          v-for="(movie, index) in wishlistMovies" 
          :key="movie.id" 
          class="wish-items"
          :style="getRowDelay(index)"
          @click="goToMovieDetail(movie.id)"
        >
          <div class="poster-container">
            <img :src="tmdb_base_url + movie.poster_path" alt="movie-poster" />
          </div>
          <h4>{{ movie.title }}</h4>
          <div class="genre-badges">
            <span 
              v-for="genre in movie.genres" 
              :key="genre.id" 
              class="genre-badge"
              :style="{ backgroundColor: getGenreColor(genre.name) }"
            >
              {{ genre.name }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { useRouter } from "vue-router";

  defineProps(['activeList', 'watchedMovies', 'wishlistMovies']);
  const emit = defineEmits(['switchList']);
  const router = useRouter();

  const switchTo = (listName) => {
  emit('switchList', listName);
  };

  const goToReviewDetail = (movieId, reviewId) => {
  router.push({ name: "ReviewDetailView", params: { moviePk: movieId, reviewPk: reviewId } });
  };

  const goToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetailView", params: { moviePk: movieId } });
  };

  const tmdb_base_url = "https://image.tmdb.org/t/p/w500"

  const getGenreColor = (genre) => {
  const genreColors = {
    '액션': '#FF6B6B',
    '모험': '#4ECDC4',
    '애니메이션': '#45B7D1',
    '코미디': '#96CEB4',
    '범죄': '#D4A5A5',
    '다큐멘터리': '#9FA8DA',
    '드라마': '#FFD93D',
    '가족': '#98DBC6',
    '판타지': '#E4C1F9',
    '역사': '#A8E6CF',
    'SF': '#3F72AF',
    '스릴러': '#364F6B',
    '전쟁': '#8785A2',
    '서부': '#DCC7AA'
  };
  return genreColors[genre] || '#6c757d';
  };

  const getItemDelay = (index) => {
  return `animation-delay: ${index * 0.2}s;`;
  };

  const getRowDelay = (index) => {
  const rowNumber = Math.floor(index / 3);
  return `animation-delay: ${rowNumber * 0.2}s;`;
  };
</script>

<style scoped>
@import "@/assets/styles/components/profileReaction.css";
</style>