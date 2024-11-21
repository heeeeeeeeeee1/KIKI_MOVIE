<template>
  <div class="page--review">
    <main class="review-container">
      <ReviewDetail
        :title="title"
        :poster="poster"
        :author="author"
        :date="date"
        :content="content"
        :isAuthor="isAuthor"
        @delete="deleteReview"
      />
      <ReviewReaction
        :likes="likes"
        @like="handleLike"
        @toggleComment="toggleCommentForm"
      />
      <ReviewComments :comments="comments" @deleteComment="deleteComment" />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ReviewDetail from "@/components/ReviewDetail.vue";
import ReviewReaction from "@/components/ReviewReaction.vue";
import ReviewComments from "@/components/ReviewComments.vue";

const title = ref("영화 제목");
const poster = ref("");

const author = ref("작성자");
const date = ref("2024-11-21");
const content = ref("최고 기깔난 영화");
const isAuthor = ref(true);

const likes = ref(10);

const comments = ref([
  { id: 1, author: "이제훈", content: "첫 번째 댓글" },
  { id: 2, author: "노진원", content: "두 번째 댓글" },
]);

const deleteReview = () => {
  console.log("리뷰 삭제");
};

const handleLike = () => {
  likes.value++;
};

const toggleCommentForm = () => {
  console.log("댓글 폼 열기/닫기");
};

const deleteComment = (id) => {
  comments.value = comments.value.filter((comment) => comment.id !== id);
};
</script>

<style>
.page--review {
  width: 100%;
  display: flex;
  justify-content: center;
}

.review-container {
  width: 60%;
  margin: auto 0;
  background-color: inherit;
}
</style>
