<template>
  <div class="review-detail-container">
    <section class="detail-left">
      <div class="info-review">
        <div>
          <span>{{ author }}</span>
          <span>{{ date }}</span>
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
          src="https://i.namu.wiki/i/78uTXq-Jd3ME_MYXtiyOo-qBPjwpiNF9qs1ko9YvE1BmaVagE9-h95a5Xuh0jVt6WX9sY8seQLZlU2GidF7Gcg.webp"
          alt="포스터 이미지"
        />
      </div>
      <button v-if="isAuthor" @click="deleteReview">댓글 삭제</button>
    </section>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

// Props 정의
defineProps(["title", "author", "date", "content", "isAuthor"]);

// Emits 정의
const emit = defineEmits(["delete"]);

// 리뷰 삭제 함수
const deleteReview = () => {
  emit("delete");
};

// 날짜 계산 표시 함수
</script>

<style scoped>
@import "@/assets/styles/components/reviewDetail.css";
</style>
