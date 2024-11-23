<!-- boxOfficeSlide -->
<template>
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
      >
        <img :src="movie.poster" alt="Movie Poster" />
        <p class="title">{{ movie.movieNm }}</p>
        <p class="rank">Rank: {{ movie.rank }}</p>
      </div>
    </div>
    <button class="arrow right-arrow" @click="nextSlide">›</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getBoxOfficeWithPosters } from "@/api/boxOfficeApi";

const movies = ref([]);
const currentIndex = ref(2);

const getStyle = (index) => {
  const offset = index - currentIndex.value;
  return {
    zIndex: movies.value.length - Math.abs(offset),
    transform: `translateX(${offset * 200}px) scale(${index === currentIndex.value ? 1.5 : 1})`,
  };
};

const hoverToCenter = (index) => {
  currentIndex.value = index;
};

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + movies.value.length) % movies.value.length;
};

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % movies.value.length;
};

onMounted(async () => {
  movies.value = await getBoxOfficeWithPosters();
});
</script>


<style scoped>
  @import "@/assets/styles/components/mainBoxOfficeSlide.css";
</style>
