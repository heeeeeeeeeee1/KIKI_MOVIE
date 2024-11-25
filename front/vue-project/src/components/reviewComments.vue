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
              <span>{{ comment.user }}</span>
              <button v-if="isCommentAuthor(comment)" @click="deleteComment(comment.id)">x</button>
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
import { useMovieStore } from "@/stores/movieStore";

const store = useMovieStore();
const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(["deleteComment"]);

const isCommentAuthor = (comment) => {
  // 현재 사용자와 댓글 작성자 비교
  return comment.user === store.currentUser;
};

const deleteComment = (id) => {
  emit("deleteComment", id);
};
</script>


<style scoped>
@import "@/assets/styles/components/reviewComments.css";
</style>
