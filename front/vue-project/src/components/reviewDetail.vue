<template>
  <div class="review-detail-container">
    <section class="detail-left">
      <div class="info-review">
        <div>
          <span>{{ author }}</span>
          <span>{{ formattedDate }}</span>
        </div>
        <div class="score-genres">
          <span>평점: {{ score }}점</span>
          <span>장르: {{ genres.join(', ') }}</span>
        </div>
      </div>
      <div class="content-review">
        <h2>{{ title }}</h2>
        <div>{{ content }}</div>
      </div>
    </section>
    <section class="detail-right">
      <div>
        <img
          :src="getPosterUrl(poster)"
          :alt="title + ' 포스터'"
        />
      </div>
      <button v-if="isAuthor" @click="deleteReview">리뷰 삭제</button>
    </section>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from "vue";

const props = defineProps({
  title: String,
  author: String,
  date: String,
  content: String,
  isAuthor: Boolean,
  score: Number,
  genres: {
    type: Array,
    default: () => []
  },
  poster: String
});

const emit = defineEmits(["delete"]);

const formattedDate = computed(() => {
  return new Date(props.date).toLocaleDateString();
});

const getPosterUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : '/default-poster.jpg';
};

const deleteReview = () => {
  emit("delete");
};
</script>

<style scoped>
@import "@/assets/styles/components/reviewDetail.css";
</style>
