<template>
  <div class="movie-reaction">
    <button @click="openReviewForm">리뷰 남기기</button>
    <button :class="{ active: isWishlist }" @click="toggleWishlist">
      보고 싶어요
    </button>
    <!-- <ReviewFormModal v-if="showReviewForm" @close="showReviewForm = false" /> -->
  </div>
</template>

<script setup>
import { ref } from "vue";
// import ReviewFormModal from './ReviewFormModal.vue';

const showReviewForm = ref(false);
const isWishlist = ref(false);

function openReviewForm() {
  showReviewForm.value = true;
}

function toggleWishlist() {
  isWishlist.value = !isWishlist.value;
}
</script>

<style scoped>
@import "@/assets/styles/components/movieReaction.css";
</style>
