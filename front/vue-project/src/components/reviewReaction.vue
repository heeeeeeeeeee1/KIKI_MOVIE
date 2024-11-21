<template>
  <div class="review-reaction-container">
    <button @click="handleLike">좋아요 {{ likes }}</button>
    <button @click="toggleCommentForm">댓글</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

// Props 정의
defineProps(["likes"]);

// Emits 정의
const emit = defineEmits(["like", "toggleComment"]);

// 좋아요 클릭 핸들러
const handleLike = () => {
  emit("like");
};

// 댓글 폼 토글 핸들러
const toggleCommentForm = () => {
  emit("toggleComment");
};
</script>

<style scoped>
@import "@/assets/styles/components/reviewReaction.css";
</style>
