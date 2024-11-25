<template>
  <div class="page--review">
    <main class="review-container">
      <div v-if="singleReview" class="review-content">
        <!-- 리뷰 상단 정보 -->
        <div class="review-header">
          <div class="user-info">
            <span class="username">{{ singleReview.user }}</span>
            <span class="date">{{ formatDate(singleReview.created_at) }}</span>
          </div>
          <div class="review-actions" v-if="isAuthor">
            <button @click="deleteReview" class="delete-btn">삭제</button>
          </div>
        </div>

        <!-- 리뷰 본문 -->
        <div class="review-main">
          <div class="review-text">
            <div class="movie-title">{{ singleReview.movie.title }}</div>
            <div class="score">평점: {{ singleReview.score }}점</div>
            <div class="genres">장르: {{ singleReview.movie_genres.join(', ') }}</div>
            <div class="content">{{ singleReview.content }}</div>
          </div>
          <div class="movie-poster">
            <img :src="`https://image.tmdb.org/t/p/w500${singleReview.movie.poster_path}`" :alt="singleReview.movie.title" />
          </div>
        </div>

        <!-- 리뷰 반응 -->
        <div class="review-reactions">
          <button @click="handleLike" class="like-btn">
            좋아요 {{ singleReview.like_count }}
          </button>
          <button @click="toggleCommentForm" class="comment-btn">
            댓글 {{ singleReview.comment_count }}
          </button>
        </div>

        <!-- 댓글 섹션 -->
        <div class="comments-section">
          <div v-if="singleReview.comments.length === 0" class="no-comments">
            <p>첫 댓글을 작성해보세요</p>
          </div>
          <div v-else class="comments-list">
            <div v-for="comment in singleReview.comments" :key="comment.id" class="comment">
              <div class="comment-header">
                <span class="comment-author">{{ comment.user }}</span>
                <button v-if="isCommentAuthor(comment)" @click="deleteComment(comment.id)" class="delete-comment">×</button>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="loading">
        리뷰를 불러오는 중...
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useRoute } from 'vue-router';
import { useMovieStore } from "@/stores/movieStore.js";

const route = useRoute();
const store = useMovieStore();
const { singleReview, getSingleReview } = store;

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const isAuthor = computed(() => {
  return false; // 현재 로그인한 사용자와 비교 로직 필요
});

const isCommentAuthor = (comment) => {
  return false; // 현재 로그인한 사용자와 비교 로직 필요
};

const handleLike = () => {
  console.log("좋아요 처리");
};

const toggleCommentForm = () => {
  console.log("댓글 폼 토글");
};

const deleteComment = (id) => {
  console.log("댓글 삭제:", id);
};

const deleteReview = () => {
  console.log("리뷰 삭제");
};

onMounted(() => {
  getSingleReview(route.params.reviewPk);
});
</script>

<style scoped>
.page--review {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.review-container {
  width: 900px;
  max-width: 90%;
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.username {
  font-weight: bold;
}

.date {
  color: #666;
}

.review-main {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.review-text {
  flex: 1;
}

.movie-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.score, .genres {
  margin-bottom: 0.5rem;
  color: #666;
}

.content {
  margin-top: 1rem;
  line-height: 1.6;
}

.movie-poster {
  width: 200px;
  flex-shrink: 0;
}

.movie-poster img {
  width: 100%;
  border-radius: 4px;
}

.review-reactions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.like-btn, .comment-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.comments-section {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}

.comment {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: bold;
}

.delete-btn, .delete-comment {
  padding: 0.25rem 0.5rem;
  border: none;
  background: #ff4444;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.delete-comment {
  background: transparent;
  color: #666;
}

.no-comments {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>