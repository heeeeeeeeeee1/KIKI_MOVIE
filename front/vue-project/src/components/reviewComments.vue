<template>
  <div class="comments-container">
    <div v-if="comments.length === 0">
      <div>
        <p>처음으로 댓글을 남겨보세요</p>
      </div>
    </div>
    <div v-else>
      <div v-for="comment in comments" :key="comment.id">
        <article class="comment-box">
          <div class="comment">
            <div>
              <span>{{ comment.author }}</span>
              <button @click="deleteComment(comment.id)">x</button>
            </div>
            <div>{{ comment.content }}</div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

// Props 정의
defineProps(["comments"]);

// Emits 정의
const emit = defineEmits(["deleteComment"]);

// 댓글 삭제 함수
const deleteComment = (id) => {
  emit("deleteComment", id);
};
</script>

<style scoped>
@import "@/assets/styles/components/reviewComments.css";
</style>
