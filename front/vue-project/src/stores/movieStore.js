// movieStore.js
import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useMovieStore = defineStore('movieStore', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(localStorage.getItem('token')); // 인증 토큰
  
  const movies = ref([]) // 단일 영화 데이터 저장
  const reviews = ref([]); // 리뷰 리스트
  const singleReview = ref(null) // 단일 리뷰 데이터

  // 영화 정보 가져오기
  const getMovies = function (moviePk) {
    axios({
      method: "get",
      url: `${API_URL}/movies/${moviePk}/detail/`,
      headers: { 
        Authorization: `Token ${token.value}`
      },
    })  
    .then((res) => {
      movies.value = res.data // 영화데이터 저장
      reviews.value = res.data.reviews; // 리뷰 리스트 저장
    })
    .catch((err) => {
      console.error("영화 데이터를 가져오는 중 오류:", err.response?.data || err.message)
    })
  }


  // 리뷰 정보 가져오기
  const getSingleReview = function (moviePk, reviewPk) {
    axios({
      method: "get",
      url: `${API_URL}/movies/${moviePk}/review/${reviewPk}/`,
      headers: { 
        Authorization: `Token ${token.value}`,
      },
    })  
    .then((res) => {
      singleReview.value = res.data
    })
    .catch((err) => {
      console.error('단일 리뷰를 가져오는 중 오류:', err.response?.data || err.message)
    })
  }
  return { movies, reviews, API_URL, token, getMovies, getSingleReview }
})
