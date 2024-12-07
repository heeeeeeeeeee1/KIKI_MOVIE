<template>
  <div class="reviews-container">
    <!-- 비로그인 상태일 때 -->
    <div v-if="!store.isLogin" class="login-prompt">
      <h2>사용자들의 리뷰를 보고싶다면 로그인해주세요!</h2>
      <button class="login-button" @click="goToLogin">로그인 하러가기</button>
    </div>

    <!-- 로그인 상태일 때 -->
    <template v-else>
      <h1 class="reviews-title">모든 리뷰</h1>
      <div v-if="!movieStore.isLoading" class="reviews-list">
        <div v-for="review in movieStore.allReviews" :key="review.id"
          :class="['review-item', { 'my-review': review.user === store.username }]">
          <!-- 기존 리뷰 관련 템플릿 코드 -->
          <template v-if="review.user !== store.username">
            <div class="profile-section">
              <img src="https://via.placeholder.com/40" alt="프로필 이미지" class="profile-image" />
              <span class="username">{{ review.user }}</span>
            </div>
          </template>

          <div class="review-bubble" @click="goToReviewDetail(review.movie.id, review.id)">
            <div class="review-content">{{ truncateContent(review.content) }}</div>
            <div class="review-footer">
              <div class="rating">
                <span v-for="n in 5" :key="n" class="star">
                  {{ n <= review.score ? '★' : '☆' }}
                </span>
              </div>
              <div class="stats">
                <span class="likes">❤ {{ review.like_count }}</span>
                <span class="comments">💬 {{ review.comment_count }}</span>
              </div>
            </div>
            <div class="movie-info">
              영화 
              <span class="movie-title-wrapper">
                <span class="movie-title">{{ review.movie.title }}</span>
                <span class="movie-title-cover"></span>
              </span>
              에 대한 리뷰입니다
            </div>
          </div>
        </div>
      </div>
      <div v-else class="loading">
        로딩 중...
      </div>
    </template>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useMovieStore } from '@/stores/movieStore';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const movieStore = useMovieStore();
const store = useCounterStore();
const router = useRouter();

const goToLogin = () => {
  router.push({ name: 'LogInView' });
};

const goToReviewDetail = (movieId, reviewId) => {
  router.push({
    name: 'ReviewDetailView',
    params: {
      moviePk: movieId,
      reviewPk: reviewId
    }
  });
};

const truncateContent = (content) => {
  if (content.length <= 100) return content;
  return content.slice(0, 100) + '...';
};

onMounted(() => {
  if (store.isLogin) {
    movieStore.fetchAllReviews();
  }
});
</script>

<style scoped>
.reviews-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.reviews-title {
  margin-bottom: 3rem;
  text-align: center;
  color: white;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 1rem;
}

.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
}

.review-bubble {
  position: relative;
  background: white;
  padding: 1rem;
  border-radius: 1rem;
  cursor: pointer;
  width: 80%;
  transition: transform 0.2s;
}

/* 일반 리뷰 (왼쪽 배치) */
.review-item:not(.my-review) .review-bubble {
  margin-left: 1rem;
}

/* 내 리뷰 (오른쪽 배치) */
.my-review {
  align-items: flex-end;
}

.my-review .review-bubble {
  background: #e3f2fd;
  margin-right: 1rem;
}

.review-bubble:hover {
  transform: translateY(-2px);
}

.review-content {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

.rating {
  color: #ffd700;
}

.stats {
  display: flex;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.movie-info {
  position: relative;
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.5rem;
  text-align: right;
}

.movie-title-wrapper {
  position: relative;
  display: inline-block;
}

.movie-title {
  position: relative;
}

.movie-title-cover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: black;
  transition: opacity 0.2s;
  z-index: 1;
}

.review-bubble:hover .movie-title-cover {
  opacity: 0;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: white;
}

.star {
  display: inline-block;
  margin-right: 2px;
}

/* 로그인 안내 섹션 스타일 */
.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  gap: 2rem;
}

.login-prompt h2 {
  color: white;
  font-size: 1.5rem;
  font-weight: 500;
}

.login-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 0.5rem;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #2980b9;
}
</style>