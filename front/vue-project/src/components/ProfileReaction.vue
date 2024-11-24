<!-- ProfileReaction -->
<template>
  <div class="profile-reaction">
    <!-- 버튼 -->
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

  <!-- 봤어요 -->
  <div class="watched-info" v-if="activeList === 'watched'">
    <div
      v-for="review in watchedMovies"
      :key="review.id"
      class="watched-items"
      @click="goToReviewDetail(review.movie.id, review.id)"
    >
      <img :src="tmdb_base_url + review.movie.poster_path" alt="movie-poster" />
      <h4>{{ review.movie.title }}</h4>
      <div class="genre-badges">
        <span v-for="genre in review.movie_genres" :key="genre" class="genre-badge">
          {{ genre }}
        </span>
      </div>
      <p>평점: {{ review.score }}</p>
      <p>리뷰: {{ review.content }}</p>
      <p>댓글: {{ review.comment_count }}개</p>
      <p>좋아요: {{ review.like_count }}개</p>
    </div>
  </div>

  <div class="wish-info">
    <!-- 보고싶어요 -->
    <div v-if="activeList === 'wishlist'" class="wish-list">
      <!-- 보고싶어요 항목 클릭 시 해당 영화 상세 페이지로 이동 -->
      <!-- 영화 타이틀, 포스터 이미지만 가져올 것 -->
      <div 
        v-for="movie in wishlistMovies" 
        :key="movie.id" 
        class="wish-items"
        @click="goToMovieDetail(movie.id)"
      >
        <img :src="tmdb_base_url + movie.poster_path" alt="movie-poster" class="wish-poster" />
        <div class="wish-details">
          <h4>{{ movie.title }}</h4>
          <div class="genre-badges">
          <span v-for="genre in movie.genres" :key="genre.id" class="genre-badge">
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
// 리스트 전환
const switchTo = (listName) => {
  emit('switchList', listName);
};

// "봤어요" 상세 페이지로 이동
const goToReviewDetail = (movieId, reviewId) => {
  router.push({ name: "ReviewDetailView", params: { moviePk: movieId, reviewPk: reviewId } });
};

// "보고싶어요" 영화 상세 페이지로 이동
const goToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetailView", params: { moviePk: movieId } });
};

const tmdb_base_url = "https://image.tmdb.org/t/p/w500"
// 더미 데이터 (사용자 영화 정보)
// const watchedMovies = [
//   { id: 1, title: '영화 A', poster: 'https://via.placeholder.com/100x150', review: '킬링타임용', score: 4 },
//   { id: 2, title: '영화 B', poster: 'https://via.placeholder.com/100x150', review: '가족영화', score: 2 },
// ];

// const wishlistMovies = [
//   { id: 3, title: '영화 C', poster: 'https://via.placeholder.com/100x150' },
//   { id: 4, title: '영화 D', poster: 'https://via.placeholder.com/100x150' },
// ];
</script>

<style scoped>
@import "@/assets/styles/components/profileReaction.css";
</style>