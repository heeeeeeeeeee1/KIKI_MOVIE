// movieStore.js
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
  const reviews = ref([]); // 리뷰 리스트
  const singleReview = ref(null); // 단일 리뷰 데이터

  console.log("현재 저장된 토큰:", token); // 토큰 확인용 로그

  // 단일 영화 정보 가져오기(로그인X)
  const getMovie = function (moviePk) {
    axios({
      method: "get",
      url: `${API_URL}/movies/${moviePk}/detail/`,
    })
      .then((res) => {
        movie.value = res.data; // 영화데이터 저장
        reviews.value = res.data.reviews; // 리뷰 리스트 저장
        console.log(movie.value);
      })
      .catch((err) => {
        console.error("영화 데이터를 가져오는 중 오류:", err.response?.data || err.message);
      });
  };

  // 리뷰 정보 가져오기(로그인X)
  const getSingleReview = function (moviePk, reviewPk) {
    axios({
      method: "get",
      url: `${API_URL}/movies/${moviePk}/review/${reviewPk}/`,
    })
      .then((res) => {
        singleReview.value = res.data;
      })
      .catch((err) => {
        console.error(
          "단일 리뷰를 가져오는 중 오류:",
          err.response?.data || err.message
        );
      });
  };

  // 리뷰 작성(로그인O)
  const createReview = function (moviePk, content, score) {
    axios({
      method: "post",
      url: `${API_URL}/movies/${moviePk}/review/create/`,
      data: { content, score },
      headers: { Authorization: `Token ${token.value}` },
    })
      .then((res) => {
        alert("리뷰 작성 성공!");
        reviews.value.push(res.data); // 작성된 리뷰를 상태에 추가
      })
      .catch((err) => {
        console.error("리뷰 작성 실패:", err.response?.data || err.message);
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
    API_URL,
    getMovie,
    getSingleReview,
    createReview,
    createComment,
  };
});
