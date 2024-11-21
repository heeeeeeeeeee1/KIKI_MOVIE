<template>
  <div class="reviews-title">
    <h3>리뷰</h3>
    <ul class="review-list">
      <li
        v-for="review in reviews"
        :key="review.id"
        @click="goToReviewDetail(review.id)"
        class="review-item"
      >
        <div class="item__author">{{ review.author }}</div>
        <div class="item__desc-container">
          <div class="item__content">
            {{ review.content }}
          </div>
        </div>
        <div class="item__reaction">
          <span>
            이모지
            {{ review.likes }}
          </span>
          <span>
            댓글
            {{ review.comments }}
          </span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const reviews = ref([
  { id: 1, author: "차은우", content: "좋은 영화!", likes: 10, comments: 2 },
  { id: 2, author: "강동원", content: "별로였어요.", likes: 3, comments: 0 },
  {
    id: 3,
    author: "장동윤",
    content:
      "아무리 생각해도 신기하다. 김태리를 모티브로 만화를 그렸는데? 그 만화가 영상화되기로 했고? 원래 웹드라마로 제작될 예정이던 작품이? 우여곡절 끝에 사이즈가 되레 커지더니?",
    likes: 10,
    comments: 2,
  },
  { id: 4, author: "정해인", content: "좋은 영화!", likes: 10, comments: 2 },
  { id: 5, author: "유승호", content: "좋은 영화!", likes: 10, comments: 2 },
  { id: 6, author: "수지", content: "좋은 영화!", likes: 10, comments: 2 },
  { id: 7, author: "신혜선", content: "좋은 영화!", likes: 10, comments: 2 },
  { id: 8, author: "조보아", content: "좋은 영화!", likes: 10, comments: 2 },
]);

function goToReviewDetail(reviewId) {
  router.push(`/movies/detail/${reviewId}`);
}
</script>

<style scoped>
@import "@/assets/styles/components/movieReviewList.css";
</style>
