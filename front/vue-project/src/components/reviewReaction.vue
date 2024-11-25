<template>
  <div class="review-reaction-container">
    <button @click="handleLike">
      좋아요 {{ likes }}
    </button>
    <button @click="toggleCommentForm">
      댓글 {{ commentCount }}
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  likes: {
    type: Number,
    default: 0
  },
  commentCount: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(["like", "toggleComment"]);

const handleLike = () => {
  emit("like");
};

const toggleCommentForm = () => {
  emit("toggleComment");
};
</script>

<style scoped>
@import "@/assets/styles/components/reviewReaction.css";
</style>
