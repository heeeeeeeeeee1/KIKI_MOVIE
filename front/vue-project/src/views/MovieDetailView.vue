<template>
  <div class="movie-detail-view">
    <div class="movie-container">
      <!-- 데이터가 없을 경우 에러 메시지 표시 -->
      <div v-if="error" class="error-message">
        <div class="siri-container">
          <div class="morph-layer layer-1"></div>
          <div class="morph-layer layer-2"></div>
          <div class="morph-layer layer-3"></div>
        </div>
        <h3>해당 ID에 대한 영화 데이터가 없습니다</h3>
      </div>
      <!-- 데이터가 있을 경우 영화 정보 및 리뷰 표시 -->
      <div v-else>
        <MovieInfo :movie="movieStore.movie" />
        <ReviewList />
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieInfo from "@/components/movieInfo.vue";
import ReviewList from "@/components/movieReviewList.vue";
</script>

<style scoped>
@import "@/assets/styles/components/noDataCircle.css";

.movie-detail-view {
  width: 100%;
  display: flex;
  justify-content: center;
}
.movie-container {
  width: 60%;
  margin: auto 0;
  background-color: inherit;
  color: white;
}
</style>
