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

  <div class="watched-info">
    <!-- 봤어요 -->
    <div v-if="activeList === 'watched'" class="watched-list">
      <div v-for="movie in watchedMovies" :key="movie.id" class="watched-items">
        <img :src="movie.poster" alt="movie-poster" class="watched-poster" />
        <div class="watched-details">
          <h4>{{ movie.title }}</h4>
          <p>내 평가:{{ movie.score }}</p>
          <p>{{ movie.review }}</p>

        </div>
      </div>
    </div>
  </div>

  <div class="wish-info">
    <!-- 보고싶어요 -->
    <div v-if="activeList === 'wishlist'" class="wish-list">
      <div v-for="movie in wishlistMovies" :key="movie.id" class="wish-items">
        <img :src="movie.poster" alt="movie-poster" class="wish-poster" />
        <div class="wish-details">
          <h4>{{ movie.title }}</h4>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['activeList']);
const emit = defineEmits(['switchList']);


// 봤어요, 보고싶어요 리스트 전환
const switchTo = (listName) => {
  emit('switchList', listName);
};

// 더미 데이터 (사용자 영화 정보)
const watchedMovies = [
  { id: 1, title: '영화 A', poster: 'https://via.placeholder.com/100x150', review: '킬링타임용', score: 4 },
  { id: 2, title: '영화 B', poster: 'https://via.placeholder.com/100x150', review: '가족영화', score: 2 },
];

const wishlistMovies = [
  { id: 3, title: '영화 C', poster: 'https://via.placeholder.com/100x150' },
  { id: 4, title: '영화 D', poster: 'https://via.placeholder.com/100x150' },
];


</script>

<style scoped>
@import "@/assets/styles/components/profileReaction.css";
</style>