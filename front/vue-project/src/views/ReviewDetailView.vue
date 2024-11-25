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
          <button
            :class="{ 'liked': isLiked }" 
            @click="handleLike"
            class="like-btn">
            좋아요 {{ likeCount }}
          </button>
          <button @click="toggleCommentForm" class="comment-btn">
            댓글 {{ singleReview.comment_count }}
          </button>
        </div>

        <div v-if="showCommentForm" class="modal">
          <div class="modal-content">
            <h3>댓글 작성</h3>
            <textarea
              v-model="newComment"
              placeholder="댓글을 입력하세요"
              class="comment-input"
            ></textarea>
            <button @click="submitComment">등록</button>
            <button @click="toggleCommentForm">취소</button>
          </div>
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
import { ref, onMounted, computed } from "vue";
import { useRoute } from 'vue-router';
import { useMovieStore } from "@/stores/movieStore.js";
import { storeToRefs } from 'pinia';

const route = useRoute();
const store = useMovieStore();

const singleReview = computed(() => store.singleReview);
const isLiked = computed(() => singleReview.value?.liked || false);
const likeCount = computed(() => singleReview.value?.like_count || 0);
const { getSingleReview, toggleLikeReview } = store;

const showCommentForm = ref(false);
const newComment = ref("");

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const isAuthor = computed(() => {
  return false; // 현재 로그인한 사용자와 비교 로직 필요
});

const isCommentAuthor = (comment) => {
  return false; // 현재 로그인한 사용자와 비교 로직 필요
};

const handleLike = async () => {
  const reviewPk = route.params.reviewPk;
  if (!reviewPk) return;
  
  try {
    await store.toggleLikeReview(reviewPk);
    await store.getSingleReview(reviewPk); // 리뷰 데이터 새로 불러오기
  } catch (err) {
    console.error("좋아요 토글 실패:", err);
  }
};

const toggleCommentForm = () => {
  showCommentForm.value = !showCommentForm.value;
};

const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  try {
    await store.createComment(route.params.reviewPk, newComment.value);
    await store.getSingleReview(route.params.reviewPk); // 댓글 작성 후 리뷰 데이터 새로고침
    newComment.value = ''; // 입력 필드 초기화
    toggleCommentForm(); // 모달 닫기
    console.log("댓글 작성 완료");
  } catch (error) {
    console.error("댓글 작성 실패:", error.response?.data || error.message);
    alert("댓글 작성 중 오류가 발생했습니다.");
  }
};


const deleteComment = (id) => {
  console.log("댓글 삭제:", id);
};

const deleteReview = () => {
  console.log("리뷰 삭제");
};

const isLoading = ref(false);

onMounted(() => {
  isLoading.value = true;
  getSingleReview(route.params.reviewPk)
    .then(() => {
      isLoading.value = false;
      console.log("리뷰 데이터를 성공적으로 가져왔습니다.");
    })
    .catch((err) => {
      console.error("리뷰 데이터를 가져오는 중 오류:", err);
      isLoading.value = false;
    });
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

.like-btn.liked {
  background-color: #ffcccc;
  border-color: #ff6666;
  color: white;
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

.review-detail {
  max-width: 800px;
  margin: 0 auto;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}
.comment-input {
  width: 100%;
  min-height: 100px;
  margin: 1rem 0;
}
</style>