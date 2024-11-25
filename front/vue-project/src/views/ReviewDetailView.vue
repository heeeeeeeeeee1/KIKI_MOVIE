<!-- ReviewDetailView.vue -->
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
            <button @click="openEditModal" class="edit-btn">수정</button>
            <button @click="confirmDelete" class="delete-btn">삭제</button>
          </div>
        </div>
        <!-- 리뷰 수정 모달 -->
        <div v-if="showEditModal" class="modal">
          <div class="modal-content">
            <h3>리뷰 수정</h3>
            <div class="edit-form">
              <div class="score-input">
                <label>평점</label>
                <input type="number" v-model="editForm.score" min="1" max="5" step="1" />
              </div>
              <textarea
                v-model="editForm.content"
                class="content-input"
                placeholder="리뷰 내용을 입력하세요"
              ></textarea>
              <div class="modal-actions">
                <button @click="submitEdit" class="submit-btn">수정</button>
                <button @click="closeEditModal" class="cancel-btn">취소</button>
              </div>
            </div>
          </div>
        </div>
        <!-- 리뷰 본문 -->
        <div class="review-main">
          <div class="review-text">
            <router-link 
              :to="{ name: 'MovieDetailView', params: { moviePk: singleReview.movie.id }}" 
              class="movie-title-link"
            >
              <div class="movie-title">{{ singleReview.movie.title }}</div>
            </router-link>
            <div class="score">평점: {{ singleReview.score }}점</div>
            <div class="genres">장르: {{ singleReview.movie_genres.join(', ') }}</div>
            <div class="content">{{ singleReview.content }}</div>
          </div>
          <router-link 
            :to="{ name: 'MovieDetailView', params: { moviePk: singleReview.movie.id }}" 
            class="movie-poster"
          >
            <img 
              :src="`https://image.tmdb.org/t/p/w500${singleReview.movie.poster_path}`" 
              :alt="singleReview.movie.title"
            />
          </router-link>
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
                <div v-if="isCommentAuthor(comment)" class="comment-actions">
                  <button @click="openEditCommentModal(comment)" class="edit-comment">수정</button>
                  <button @click="confirmDeleteComment(comment.id)" class="delete-comment">×</button>
                </div>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </div>
        <!-- 댓글 수정 모달 -->
        <div v-if="showEditCommentModal" class="modal">
          <div class="modal-content">
            <h3>댓글 수정</h3>
            <textarea
              v-model="editCommentForm.content"
              class="comment-input"
              placeholder="댓글 내용을 입력하세요"
            ></textarea>
            <div class="modal-actions">
              <button @click="submitCommentEdit" class="submit-btn">수정</button>
              <button @click="closeEditCommentModal" class="cancel-btn">취소</button>
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
import { useRoute, useRouter } from 'vue-router';
import { useMovieStore } from "@/stores/movieStore.js";
import { storeToRefs } from 'pinia';
import { useCounterStore } from '@/stores/counter';

const route = useRoute();
const router = useRouter();
const store = useMovieStore();
const counterStore = useCounterStore();

const singleReview = computed(() => store.singleReview);
const isLiked = computed(() => singleReview.value?.liked || false);
const likeCount = computed(() => singleReview.value?.like_count || 0);
const { getSingleReview, toggleLikeReview } = store;

const showCommentForm = ref(false);
const newComment = ref("");

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const showEditModal = ref(false);
const editForm = ref({
  content: '',
  score: 0
});

const showEditCommentModal = ref(false);
const editCommentForm = ref({
  id: null,
  content: ''
});

const isAuthor = computed(() => {
  return singleReview.value?.user === counterStore.username;
});

const openEditModal = () => {
  editForm.value = {
    content: singleReview.value.content,
    score: singleReview.value.score
  };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
};

const submitEdit = async () => {
  try {
    await store.updateReview(route.params.reviewPk, editForm.value);
    await store.getSingleReview(route.params.reviewPk);
    closeEditModal();
  } catch (error) {
    console.error('리뷰 수정 실패:', error);
    alert('리뷰 수정 중 오류가 발생했습니다.');
  }
};

const confirmDelete = async () => {
  if (!confirm('정말로 이 리뷰를 삭제하시겠습니까?')) return;
  
  try {
    await store.deleteReview(route.params.reviewPk);
    router.push(`/movies/${singleReview.value.movie.id}`);
  } catch (error) {
    console.error('리뷰 삭제 실패:', error);
    alert('리뷰 삭제 중 오류가 발생했습니다.');
  }
};

const isCommentAuthor = (comment) => {
  return comment.user === counterStore.username;
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

const openEditCommentModal = (comment) => {
  editCommentForm.value = {
    id: comment.id,
    content: comment.content
  };
  showEditCommentModal.value = true;
};

const closeEditCommentModal = () => {
  showEditCommentModal.value = false;
  editCommentForm.value = { id: null, content: '' };
};

const submitCommentEdit = async () => {
  if (!editCommentForm.value.content.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  try {
    await store.updateComment(editCommentForm.value.id, editCommentForm.value.content);
    await store.getSingleReview(route.params.reviewPk);
    closeEditCommentModal();
  } catch (error) {
    console.error("댓글 수정 실패:", error);
    alert("댓글 수정 중 오류가 발생했습니다.");
  }
};

const confirmDeleteComment = async (commentId) => {
  if (!confirm('정말로 이 댓글을 삭제하시겠습니까?')) return;
  
  try {
    await store.deleteComment(commentId);
    await store.getSingleReview(route.params.reviewPk);
  } catch (error) {
    console.error('댓글 삭제 실패:', error);
    alert('댓글 삭제 중 오류가 발생했습니다.');
  }
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
.edit-btn {
  padding: 0.25rem 0.5rem;
  border: none;
  background: #4CAF50;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.score-input {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.content-input {
  width: 100%;
  min-height: 150px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.submit-btn {
  background: #4CAF50;
  color: white;
}

.cancel-btn {
  background: #f44336;
  color: white;
}

.submit-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.movie-title-link {
  text-decoration: none;
  color: inherit;
}

.movie-title-link:hover .movie-title {
  color: #4CAF50;
}

.movie-poster {
  display: block;
  cursor: pointer;
  transition: transform 0.2s;
}

.movie-poster:hover {
  transform: scale(1.05);
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-comment {
  padding: 0.25rem 0.5rem;
  border: none;
  background: #4CAF50;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.delete-comment {
  padding: 0.25rem 0.5rem;
  border: none;
  background: #ff4444;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}
</style>