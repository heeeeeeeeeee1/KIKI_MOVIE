<template>
  <header>
    <div class="header-container">
      <nav class="left-menu">
        <RouterLink
          :to="{ name: 'MainHomeView' }"
          class="nav-text logo logo-accounts"
        >
          <div class="img-container">
            <img src="@/assets/logo_white.png" alt="키키무비 로고 이미지" />
          </div>
          <span>KIKI</span>
        </RouterLink>
      </nav>
      <nav class="right-users">
        <div v-if="!store.isLogin">
          <RouterLink
            :to="{ name: 'SignUpView' }"
            class="nav-text users__signup"
          >
            회원가입
          </RouterLink>
          <RouterLink :to="{ name: 'LogInView' }" class="nav-text users__login">
            로그인
          </RouterLink>
        </div>
        <div v-else>
          <!-- 최신 리뷰 말풍선 -->
          <div class="review-bubble" @click="goToReviews">
            <div class="bubble-content">
              <span 
                v-if="movieStore.latestUserReview" 
                :title="`마지막 영화 : ${movieStore.latestUserReview.movie.title}`"
              >
                {{ truncatedReview }}
              </span>
              <span v-else>
                리뷰 보러가기
              </span>
            </div>
          </div>
          <RouterLink
            :to="{ name: 'UserProfileView' }"
            class="nav-text users__login"
          >
            {{ store.username }}
          </RouterLink>
          <form @submit.prevent="logOut">
            <input
              type="submit"
              value="로그아웃"
              class="nav-text users__logout"
            />
          </form>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import { useMovieStore } from "@/stores/movieStore";

const movieStore = useMovieStore();
const store = useCounterStore();
const router = useRouter();
const error = ref(false);

const truncatedReview = computed(() => {
  if (!movieStore.latestUserReview?.content) return '';
  return movieStore.latestUserReview.content.length > 7
    ? `${movieStore.latestUserReview.content.slice(0, 7)}...`
    : movieStore.latestUserReview.content;
});

const logOut = function () {
  store.logOut();
};

const goToReviews = () => {
  router.push({ name: 'AllReviewsView' });
};

onMounted(() => {
  if (store.token) {
    store
      .fetchUserInfo()
      .then(() => {
        error.value = false;
        return movieStore.fetchLatestUserReview(store.username);
      })
      .catch((err) => {
        console.log("유저 정보 로드 실패:", err);
        error.value = true;
      });
  } else {
    console.log("유저 정보가 없습니다");
  }
});
</script>

<style scoped>
@import "@/assets/styles/components/header.css";

.user-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;  /* 컴포넌트 간 간격 증가 */
}

.review-bubble {
  position: relative;
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
  min-width: 100px;
  margin-right: 1rem;  /* 사용자 이름과의 간격 추가 */
}

.review-bubble:hover {
  background: var(--light-gray);
}

/* 말풍선 꼬리 방향 변경 */
.review-bubble::before {
  content: "";
  position: absolute;
  right: -10px;  /* left에서 right로 변경 */
  top: 50%;
  transform: translateY(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: transparent transparent transparent #f0f0f0;  /* 화살표 방향 변경 */
}

.review-bubble:hover::before {
  border-color: transparent transparent transparent #e0e0e0;  /* hover 시 색상도 변경 */
}

.bubble-content {
  font-size: 0.9rem;
  color: #333;
  text-align: center;
}
</style>
