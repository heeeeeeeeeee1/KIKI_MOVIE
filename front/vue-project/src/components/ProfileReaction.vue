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
    <!-- 봤어요 힝목 클릭 시 해당 리뷰 상세 페이지로 이동 -->
    <div v-for="movie in watchedMovies" :key="movie.id" class="watched-items">
      <!-- 영화 관련 정보 - title, poster 안나옴 -->
      <h4>{{ movie.title }}</h4>
      <p>평점: {{ movie.score }}</p>
      <p>{{ movie.content }}</p>
      <!-- 댓글과 코멘트 보이게 하기 -->
    </div>
  </div>

  <div class="wish-info">
    <!-- 보고싶어요 -->
    <div v-if="activeList === 'wishlist'" class="wish-list">
      <!-- 보고싶어요 항목 클릭 시 해당 영화 상세 페이지로 이동 -->
      <!-- 영화 타이틀, 포스터 이미지만 가져올 것 -->
      <div v-for="movie in wishlistMovies" :key="movie.id" class="wish-items">
        <img :src="tmdb_base_url + movie.poster_path" alt="movie-poster" class="wish-poster" />
        <div class="wish-details">
          <h4>{{ movie.title }}</h4>
          <!-- 장르 관련 키워드 인자 리스트업하기 -->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['activeList', 'watchedMovies', 'wishlistMovies']);
const emit = defineEmits(['switchList']);

// 리스트 전환
const switchTo = (listName) => {
  emit('switchList', listName);
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