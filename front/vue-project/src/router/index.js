import { createRouter, createWebHistory } from "vue-router";

import MainHomeView from "@/views/MainHomeView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LoginView.vue";
import ReviewDetailView from "@/views/ReviewDetailView.vue";

import { useCounterStore } from "@/stores/counter";

import MovieDetailView from "@/views/MovieDetailView.vue"; // 영화 상세 정보
import UserProfileView from "@/views/UserProfileView.vue";
import UserEditView from "@/views/UserEditView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MainHomeView",
      component: MainHomeView,
    },
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
      path: "/review/",
      name: "ReviewDetailView",
      component: ReviewDetailView,
    },
    {
      path: "/movies/:moviePk",
      name: "MovieDetailView",
      component: MovieDetailView, // 영화 상세 페이지
    },
    {
      path: "/movies/:moviePk/review/:reviewPk",
      name: "ReviewDetailView",
      component: ReviewDetailView,
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
