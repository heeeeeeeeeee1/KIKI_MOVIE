import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";
import { useCounterStore } from "@/stores/counter";

export const useMovieStore = defineStore("movieStore", () => {
  const API_URL = "http://127.0.0.1:8000";
  const counterStore = useCounterStore();
  const token = counterStore.token; // counter의 토큰 상태 참조

  const movie = ref({}); // 단일 영화 데이터 저장
  const movies = ref([]); // 영화 데이터 저장
// 아래 28번째 줄까지 CONFLICT
// movieStore.js
// import axios from 'axios'
// import { ref } from 'vue'
// import { defineStore } from 'pinia'

// export const useMovieStore = defineStore('movieStore', () => {
//   const API_URL = 'http://127.0.0.1:8000'
//   const token = ref(localStorage.getItem('token')); // 인증 토큰
  
//   const movie = ref({}) // 단일 영화 데이터 저장
//   const movies = ref([]) // 영화 데이터 저장
  const reviews = ref([]); // 리뷰 리스트
  const singleReview = ref(null); // 단일 리뷰 데이터

  // console.log("현재 저장된 토큰:", token); // 토큰 확인용 로그
  
  // 단일 영화 정보 가져오기(로그인X)
  const getMovie = function (moviePk) {
    movie.value = {}; // 초기화
    return axios({
      method: "get",
      url: `${API_URL}/movies/${moviePk}/detail/`,
    })
      .then((res) => {
        movie.value = res.data;
      })
      .catch((err) => {
        console.error("영화 데이터를 가져오는 중 오류:", err.response?.data || err.message);
      });
  };

  // 영화 보고 싶어요 상태 변경(로그인O)
  const toggleWishlist = function (moviePk) {
    if (!token) {
      router.push("/login");
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "post",
      url: `${API_URL}/movies/${moviePk}/wishlist/`,
      headers: { Authorization: `Token ${token}` },
    }).catch((err) => {
      console.error("보고싶어요 상태 변경 실패:", err.response?.data || err.message);
      throw err;
    });
  };
  
  // 리뷰 목록 가져오기(로그인X)
  const fetchMovieReviews = function (moviePk) {
    reviews.value = []; // 초기화
  
    return axios({
      method: "get",
      url: `${API_URL}/movies/${moviePk}/reviews/`,
    })
      .then((res) => {
        reviews.value = res.data || [];
        console.log("가져온 리뷰 데이터:", reviews.value);
      })
      .catch((err) => {
        reviews.value = []; // 에러 발생 시 빈 배열 유지
        console.error("리뷰 데이터를 가져오는 중 오류:", err.response?.data || err.message);
        throw err;
      });
  };

  /////////////////////// 리뷰 상세 페이지 관련 /////////////////////
  const fetchReview = () => {
    console.log("리뷰 데이터를 가져옵니다...");
    getSingleReview(1); // reviewPk만 전달
  };

  // 리뷰 정보 가져오기(로그인X)
  const isLoading = ref(false);

  const getSingleReview = function (reviewPk) {
    isLoading.value = true;
    return axios({
      method: "get",
      url: `${API_URL}/movies/reviews/${reviewPk}/`,
    })
    .then((res) => {
      singleReview.value = res.data;
    })
    .catch((err) => {
      console.error("단일 리뷰 데이터를 가져오는 중 오류:", err.response?.data || err.message);
    })
    .finally(() => {
      isLoading.value = false;
    });
  };

  const toggleLikeReview = function (reviewPk) {
    if (!token) {
      alert("로그인이 필요합니다.");
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "post",
      url: `${API_URL}/movies/reviews/${reviewPk}/like/`,
      headers: { Authorization: `Token ${token}` },
    })
      .then((res) => {
        // 현재 리뷰의 liked 상태와 like_count 업데이트
        if (singleReview.value && singleReview.value.id === reviewPk) {
          singleReview.value = {
            ...singleReview.value,
            liked: !singleReview.value.liked,
            like_count: singleReview.value.liked 
              ? singleReview.value.like_count - 1 
              : singleReview.value.like_count + 1
          };
        }
        return singleReview.value;
      })
      .catch((err) => {
        console.error("좋아요 토글 실패:", err.response?.data || err.message);
        throw err;
      });
  };

  // 리뷰 작성(로그인O)
  const createReview = function (moviePk, content, score) {
    if (!token) {
      console.error("유효한 토큰이 없습니다. 로그인이 필요합니다.");
      return Promise.reject("로그인이 필요합니다.");
    }
    return axios({
      method: "post",
      url: `${API_URL}/movies/${moviePk}/review/create/`,
      data: { content, score },
      headers: { Authorization: `Token ${token}` },
    })
    .then((res) => {
      console.log("작성된 리뷰 데이터:", res.data);
      return fetchMovieReviews(moviePk); // 서버의 최신 데이터를 가져옴
    })
    .catch((err) => {
      console.error("리뷰 작성 실패:", err.response?.data || err.message);
      throw err;
    });
  };

  // 댓글 생성(로그인O)
  const createComment = function (moviePk, reviewPk, content) {
    axios({
      method: "post",
      url: `${API_URL}/movies/${moviePk}/review/${reviewPk}/comment/create/`,
      data: { content },
      headers: { Authorization: `Token ${token.value}` },
    })
    .then((res) => {
      alert("댓글 작성 성공!");
    })
    .catch((err) => {
      console.error("댓글 작성 실패:", err.response?.data || err.message);
    });
  };

  return {
    movie,
    movies,
    reviews,
    singleReview,
    API_URL,
    getMovie,
    fetchMovieReviews,
    toggleLikeReview,
    getSingleReview,
    createReview,
    createComment,
    toggleWishlist,
  };
});
//       headers: { 
//         Authorization: `Token ${token.value}`,
//       },
//     })  
//     .then((res) => {
//       singleReview.value = res.data
//     })
//     .catch((err) => {
//       console.error('단일 리뷰를 가져오는 중 오류:', err.response?.data || err.message)
//     })
//   }
//   return { movie, movies, isLogin, reviews, API_URL, token, getMovie, getSingleReview }
// })

