<template>
  <div class="review-reaction-container">
    <button @click="handleLike">좋아요 {{ likes }}</button>
    <button @click="toggleCommentForm">댓글</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

defineProps(["likes", "isLoggedIn"]); // isLoggedIn prop 추가
const emit = defineEmits(["like", "toggleComment"]);

const handleLike = () => {
  if (!isLoggedIn) {
    alert("로그인이 필요합니다."); // 로그인 안내 메시지
    return;
  }
  emit("like");
};

const toggleCommentForm = () => {
  if (!isLoggedIn) {
    alert("로그인이 필요합니다."); // 로그인 안내 메시지
    return;
  }
  emit("toggleComment");
};
</script>

<style scoped>
@import "@/assets/styles/components/movieReaction.css";
</style>
