<template>
  <main class="main-home-container">
    <div class="main-home">
      <BoxOfficeSlide />
      <PopularReviewList />
      <MyGenrePopular />
      <MyAgePopular />
    </div>
  </main>
</template>

<script setup>
  import BoxOfficeSlide from '@/components/boxOfficeSlide.vue';
  import PopularReviewList from '@/components/popularReviewList.vue';
  import MyGenrePopular from '@/components/myGenrePopular.vue';
  import MyAgePopular from '@/components/myAgePopular.vue';
</script>

<style scoped>
  .main-home-container {
    display: flex;
    justify-content: center;
  }
  .main-home {
    width: 70%;
    overflow: hidden;
  }
</style>
