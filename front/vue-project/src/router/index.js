import { createRouter, createWebHistory } from "vue-router";
import { useCounterStore } from "@/stores/counter";

import MainHomeView from "@/views/MainHomeView.vue";

import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LoginView.vue";
import UserProfileView from "@/views/UserProfileView.vue";
import UserEditView from "@/views/UserEditView.vue";

import MovieDetailView from "@/views/MovieDetailView.vue";
import ReviewDetailView from "@/views/ReviewDetailView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 메인 페이지
    {
      path: "/",
      name: "MainHomeView",
      component: MainHomeView,
    },
    // accounts 관련 (회원 가입, 로그인, 프로필, 프로필 수정)
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: '/profile',
      name: 'UserProfileView',
      component: UserProfileView,
    },
    {
      path: '/profile/edit',
      name: 'UserEditView',
      component: UserEditView,
    },
    // movies 내 영화 상세 페이지
    {
      path: "/movies/:moviePk",
      name: "MovieDetailView",
      component: MovieDetailView, // 영화 상세 페이지
    },
    // movies 내 리뷰 상세 페이지
    {
      path: "/movies/reviews/:reviewPk",
      name: "ReviewDetailView",
      component: ReviewDetailView,
    },
    // {
    //   path: '/profile',
    //   name: 'UserProfileView',
    //   component: UserProfileView,
    // },
    // {
    //   path: '/profile/edit',
    //   name: 'UserEditView',
    //   component: UserEditView,
    // },
    // {
    //   path: "/movies/:moviePk/review/:reviewPk",
    //   name: "SingleReview",
    //   component: SingleReview, // 단일 리뷰 상세 페이지
    // },
  ],
});

router.beforeEach((to, from) => {
  const store = useCounterStore();
  if (to.name === "ArticleView" && !store.isLogin) {
    window.alert("로그인이 필요합니다.");
    return { name: "LogInView" };
  }

  if ((to.name === "SignUpView" || to.name === "LogInView") && store.isLogin) {
    window.alert("이미 로그인 되어있습니다.");
    return false;
  }
});

export default router;
