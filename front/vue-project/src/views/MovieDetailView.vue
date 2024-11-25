
<!-- MovieDetailView.vue -->
<template>
  <div class="movie-detail-view">
    <div class="movie-container">
      <!-- 데이터가 없을 경우 에러 메시지 표시 -->
      <div v-if="error" class="error-message">
        <div class="siri-container">
          <div class="morph-layer layer-1"></div>
          <div class="morph-layer layer-2"></div>
          <div class="morph-layer layer-3"></div>
        </div>
        <h3>영화 정보가 없어요<br>다른 영화를 찾아보시는 건 어떠신가요?</h3>
      </div>
      <!-- 데이터가 있을 경우 영화 정보 및 리뷰 표시 -->
      <div v-else>
        <MovieInfo :movie="movieStore.movie" />
        <div class="movie-btns">
          <button :class="{'wishlist-checked': isWishlistChecked}" @click="toggleWishlist">
            보고싶어요
          </button>
          <button @click="openModal">리뷰 작성</button>
        </div>
        <ReviewList :reviews="movieStore.reviews" />
      </div>
    </div>

    <!-- 모달 창 -->
    <div
      v-if="isModalOpen"
      class="modal"
      :class="{'shake': isShaking}"
    >
      <div class="modal-content--create-review">
        <h3> {{ counterStore.username }}님<br> "{{ movieStore.movie.title }}" 어땠나요?</h3>
        <form @submit.prevent="submitReview">
          <!-- 별점 조정 -->
          <div class="rating-input">
            <button class="rating-btns" type="button" @click="decreaseScore">-</button>
            <div class="stars">
              <span
                v-for="n in 5"
                :key="n"
                :class="{'filled-star': n <= reviewScore}"
                class="star"
              >★</span>
            </div>
            <button class="rating-btns" type="button" @click="increaseScore">+</button>
          </div>
          <!-- <p class="current-score">현재 별점: {{ reviewScore }}</p> -->
          <!-- 리뷰 내용 -->
          <textarea
            v-model="reviewContent"
            :placeholder="userReview ? userReview.content : '리뷰를 작성하세요 (100자 이내)'"
          ></textarea>
          <button class="submit-btns" type="submit">리뷰 등록</button>
          <button class="submit-btns" type="button" @click="closeModal">취소</button>
        </form>
      </div>
    </div>

    <div v-if="isConfirmModalOpen" class="modal">
      <div class="modal-content--gotoreview">
        <h3>영화를 보셨나요? 리뷰를 남겨보시겠어요?</h3>
        <button class="submit-btns" @click="confirmOpenReviewModal">리뷰 남기기</button>
        <button class="submit-btns" @click="closeConfirmModal">괜찮아요</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import MovieInfo from "@/components/movieInfo.vue";
import ReviewList from "@/components/movieReviewList.vue";
import { onMounted, ref, computed } from "vue";
import { useMovieStore } from "@/stores/movieStore";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const movieStore = useMovieStore();
const counterStore = useCounterStore();
const route = useRoute();
const router = useRouter();
const moviePk = route.params.moviePk;

const error = ref(false);

const isWishlistChecked = ref(false);
const isModalOpen = ref(false);
const isShaking = ref(false);
const reviewContent = ref("");
const reviewScore = ref(1);
const userReview = ref(null);
const userReviewCount = ref(0);
const isConfirmModalOpen = ref(false);
const isWishlistCancelScheduled = ref(false);

onMounted(() => {
  movieStore
    .getMovie(moviePk)
    .then(() => {
      error.value = false;
      isWishlistChecked.value = movieStore.movie.isInWishlist || false;

      if (movieStore.reviews?.length > 0) {
        userReview.value = movieStore.reviews.find(
          (review) => review.user === movieStore.currentUser
        );
        userReviewCount.value = userReview.value
          ? userReview.value.view_count || 1
          : 0;
        reviewContent.value = "";
      } else {
        userReview.value = null;
        userReviewCount.value = 0;
      }
    })
    .catch((err) => {
      console.error("API 호출 중 오류:", err);
      error.value = true;
    });
});

///////////////////// 보고 싶어요 관련 토글 및 모달 로직 ////////////////////
const toggleWishlist = () => {
  if (isWishlistChecked.value) {
    // 보고싶어요 상태 해제 시 확인 모달 열기
    isConfirmModalOpen.value = true;
  } else {
    // 보고싶어요 상태 설정
    movieStore.toggleWishlist(moviePk).then(() => {
      isWishlistChecked.value = true;
    });
  }
};

const confirmOpenReviewModal = () => {
  isConfirmModalOpen.value = false; // 확인 모달 닫기
  isWishlistCancelScheduled.value = true; // 해제 예약 설정
  openModal(); // 리뷰 작성 모달 열기
};


const closeConfirmModal = () => {
  isConfirmModalOpen.value = false; // 확인 모달 닫기
  movieStore.toggleWishlist(moviePk).then(() => {
    isWishlistChecked.value = false; // 보고싶어요 체크 해제
  });
};

/////////////////// 리뷰 생성 관련 모달 로직 ///////////////////////////////
const openModal = () => {
  if (!counterStore.isLogin) {
    alert("로그인이 필요합니다. 로그인 페이지로 이동합니다.");
    router.push("/login");
    return;
  }
  isModalOpen.value = true; // 모달 열기
};

const shakeModal = () => {
  isShaking.value = true; // 흔들림 활성화
  setTimeout(() => {
    isShaking.value = false; // 일정 시간 후 흔들림 비활성화
  }, 500); // 0.5초 후 종료
};

const decreaseScore = () => {
  if (reviewScore.value > 1) {
    reviewScore.value--;
  } else {
    shakeModal(); // 최솟값일 경우 모달 흔들기
  }
};

const increaseScore = () => {
  if (reviewScore.value < 5) {
    reviewScore.value++;
  } else {
    shakeModal(); // 최댓값일 경우 모달 흔들기
  }
};

const closeModal = () => {
  isModalOpen.value = false; // 리뷰 작성 모달 닫기

  if (isWishlistCancelScheduled.value) {
    // 예약된 보고싶어요 해제 처리
    movieStore.toggleWishlist(moviePk).then(() => {
      isWishlistChecked.value = false; // 보고싶어요 해제
      isWishlistCancelScheduled.value = false; // 예약 상태 초기화
    });
  }
};

const submitReview = () => {
  if (!reviewContent.value.trim()) {
    shakeModal(); // 리뷰 내용 누락 시 모달 흔들기
    return;
  }

  if (reviewScore.value < 1 || reviewScore.value > 5) {
    shakeModal(); // 별점 유효성 검증
    return;
  }

  movieStore
    .createReview(moviePk, reviewContent.value, reviewScore.value)
    .then(() => {
      isWishlistCancelScheduled.value = false; // 해제 예약 취소
      closeModal(); // 리뷰 작성 모달 닫기
    })
    .catch((err) => {
      console.error("리뷰 작성 실패:", err);
    });
};
</script>

<style scoped>
@import "@/assets/styles/components/noDataCircle.css";

.movie-detail-view {
  width: 100%;
  display: flex;
  justify-content: center;
}

.movie-container {
  width: 60%;
  margin: auto 0;
  background-color: inherit;
  color: white;
}

/* 보고싶어요, 리뷰 작성 버튼 -------------------------------------------------------- */
.movie-btns {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: 1rem;
}

.movie-btns button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.4rem;
}

.movie-btns button:first-child {
  margin-right: 1rem;
}

.movie-btns button:not(.wishlist-checked) {
  background-color: var(--light-gray);
}

.movie-btns button:hover {
  background-color: var(--real-gray);
  color: white;
}

.wishlist-checked {
  background-color: var(--light-blue);
  color: white;
}

/* 모달 (리뷰 작성, 보고싶어요 취소) ------------------------------------------ */
@keyframes shake {
  0% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-10px);
  }
  50% {
    transform: translateX(10px);
  }
  75% {
    transform: translateX(-10px);
  }
  100% {
    transform: translateX(0);
  }
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content--create-review {
  background: var(--card-black);
  border: 0.5px solid var(--real-gray);
  border-radius: 1rem;
  padding: 2rem 3rem;
  text-align: center;
}

.modal-content--gotoreview {
  background: var(--card-black);
  border: 0.5px solid var(--real-gray);
  border-radius: 1rem;
  padding: 2rem 3rem;
  text-align: center;
}

.modal h3 {
  font-size: 1.25rem;
  color: white;
  line-height: 2rem;
}

.modal.shake {
  animation: shake 0.5s ease-in-out;
}

.submit-btns {
  margin: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btns:hover {
  background-color: var(--real-gray);
  color: white;
}

/* 리뷰 생성 모달 특화 스타일 --------------------------------------------- */
.rating-input {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1.5rem 0 2rem;
}

.rating-btns {
  background-color: var(--dark-gray); 
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 20px;
  cursor: pointer;
  margin: 0 10px;
}

.rating-btns:hover {
  background-color: var(--real-gray);
}
.rating-input .stars {
  display: flex;
  gap: 5px;
}

.star {
  font-size: 30px;
  color: #ddd;
}

.filled-star {
  color: gold;
}

textarea {
  border-radius: 0.5rem;
  width: 100%;
  height: 150px;
  margin-bottom: 10px;
  padding: 0.75rem;
}
textarea:focus {
  outline: none;
}
</style>