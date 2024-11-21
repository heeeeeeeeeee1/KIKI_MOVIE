import { createRouter, createWebHistory } from "vue-router";

import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LoginView.vue";
import ReviewDetailView from "@/views/ReviewDetailView.vue";

import { useCounterStore } from "@/stores/counter";

import DetailView from "@/views/MovieDetailView.vue"; // 영화 상세 정보
// import SingleReview from "@/components/SingleReview.vue"; // 단일 리뷰 정보

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: "/movies/",
      name: "DetailView",
      component: DetailView, // 영화 상세 페이지
    },
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
    return { name: "ArticleView" };
  }
});

export default router;
