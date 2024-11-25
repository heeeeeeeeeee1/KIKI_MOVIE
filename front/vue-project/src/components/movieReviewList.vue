<template>
  <section>
    <!-- 로딩 중인 경우 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <p>리뷰 데이터를 불러오는 중입니다...</p>
      </div>
    </div>

    <!-- 로드 완료 후 콘텐츠 -->
    <div v-else>
      <h2 class="review-list__title">REVIEW</h2>
      <ul v-if="reviews && reviews.length > 0" class="review-list">
        <li
          v-for="review in reviews"
          :key="review.id"
          @click="goToReviewDetail(review.id)"
          class="review-item"
        >
          <div class="item__author-container">
            <div class="item__author">{{ review.user }}</div>
            <div class="item__rating">★ {{ review.score }}</div>
          </div>
          <div class="item__desc-container">
            <div class="item__content">{{ review.content }}</div>
          </div>
          <div class="item__reaction">
            <span>좋아요 {{ review.like_count || 0 }}</span>
            <span>댓글 {{ review.comment_count || 0 }}</span>
          </div>
        </li>
      </ul>

      <!-- 리뷰가 없는 경우 -->
      <div v-else class="no-review">
        <p>다른 사용자에게 도움이 되도록<br>이 영화의 첫인상을 만들어주세요!</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useMovieStore } from "@/stores/movieStore";
import { useRouter, useRoute } from "vue-router";

const movieStore = useMovieStore();
const reviews = computed(() => movieStore.reviews);
const route = useRoute();
const router = useRouter();

const loading = ref(true); // 로딩 상태 관리

onMounted(() => {
  const moviePk = route.params.moviePk;
  movieStore
    .fetchMovieReviews(moviePk)
    .then(() => {
      loading.value = false; // 로딩 완료
    })
    .catch((err) => {
      console.error("리뷰 데이터를 가져오는 중 오류:", err);
      loading.value = false; // 로딩 실패 시 로딩 종료
    });
});

function goToReviewDetail(reviewId) {
  router.push(`/movies/reviews/${reviewId}`);
}

// const reviews = ref([
//   { id: 1, author: "차은우", content: "좋은 영화!", likes: 10, comments: 2 },
//   { id: 2, author: "강동원", content: "별로였어요.", likes: 3, comments: 0 },
//   {
//     id: 3,
//     author: "장동윤",
//     content:
//       "아무리 생각해도 신기하다. 김태리를 모티브로 만화를 그렸는데? 그 만화가 영상화되기로 했고? 원래 웹드라마로 제작될 예정이던 작품이? 우여곡절 끝에 사이즈가 되레 커지더니?",
//     likes: 10,
//     comments: 2,
//   },
//   { id: 4, author: "정해인", content: "좋은 영화!", likes: 10, comments: 2 },
//   { id: 5, author: "유승호", content: "좋은 영화!", likes: 10, comments: 2 },
//   { id: 6, author: "수지", content: "좋은 영화!", likes: 10, comments: 2 },
//   { id: 7, author: "신혜선", content: "좋은 영화!", likes: 10, comments: 2 },
//   { id: 8, author: "조보아", content: "좋은 영화!", likes: 10, comments: 2 },
// ]);

</script>

<style scoped>
@import "@/assets/styles/components/movieReviewList.css";
</style>
