// movieStore.js
import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// 환경변수 설정
// const API_KEY = import.meta.env.VITE_TMDB_API_KEY


export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const error = ref(null) // 이거 필수야?

  const getMovieData = () => {
    axios({
      method: "get",
      url: "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1",
      headers: { 
        Authorization: 
        // api 키. 환경변수로 설정
      },
    })  
    .then((response) => {
      console.log(response.data)
    })
    .catcch((err) => {
      console.log(response.data)
    })
  }
  return { getMovieData }
})

