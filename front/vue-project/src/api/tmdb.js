import axios from "axios";
import { ref } from "vue";

const TMDB_API_KEY = "700c493de1fec79592154b7cb6361039"; // 여기에 본인의 TMDB API 키를 입력하세요.
const BASE_URL = "https://api.themoviedb.org/3";

// 인기 영화 정보 가져오기
export function useTmdb() {
  const movies = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const fetchPopularMovies = async (page = 1) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`${BASE_URL}/movie/popular`, {
        params: {
          api_key: TMDB_API_KEY,
          page,
          language: "ko-KR", // 언어를 한국어로 설정
        },
      });
      movies.value = response.data.results;
    } catch (err) {
      console.error("Failed to fetch movies:", err);
      error.value = err.message;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    movies,
    isLoading,
    error,
    fetchPopularMovies,
  };
}

// 인기 배우 가져오기
export const getPopularActors = async (page = 1) => {
  const response = await axios.get(`${BASE_URL}/person/popular`, {
    params: { 
      api_key: TMDB_API_KEY, 
      page,
      language: "ko-KR", // 언어를 한국어로 설정
    },
  });
  return response.data.results; // 배우 리스트 반환
};

// 특정 배우의 출연 영화 가져오기
export const getMoviesByActor = async (actorId) => {
  const response = await axios.get(`${BASE_URL}/person/${actorId}/movie_credits`, {
    params: { 
      api_key: TMDB_API_KEY,
      language: "ko-KR", // 언어를 한국어로 설정
    },
  });
  return response.data.cast; // 출연 영화 리스트 반환
};
