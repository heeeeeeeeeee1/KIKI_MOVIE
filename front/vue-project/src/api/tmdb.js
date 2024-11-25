import axios from "axios";
import { ref } from "vue";

const TMDB_API_KEY = "700c493de1fec79592154b7cb6361039"; // 반드시 TMDB API 키를 입력하세요.
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
  try {
    const response = await axios.get(`${BASE_URL}/person/popular`, {
      params: { 
        api_key: TMDB_API_KEY, 
        page,
        language: "ko-KR", // 언어를 한국어로 설정
      },
    });
    return response.data.results; // 배우 리스트 반환
  } catch (error) {
    console.error("Failed to fetch popular actors:", error);
    throw new Error("인기 배우 정보를 가져오는 데 실패했습니다.");
  }
};

// 특정 배우의 출연 영화 가져오기
export const getMoviesByActor = async (actorId) => {
  try {
    const response = await axios.get(`${BASE_URL}/person/${actorId}/movie_credits`, {
      params: {
        api_key: TMDB_API_KEY,
        language: "ko-KR", // 언어를 한국어로 설정
      },
    });

    // 콘솔에 응답 데이터 출력 (디버깅용)
    console.log("TMDB API 응답 데이터:", response.data.cast);

    // 응답 데이터가 없는 경우 처리
    if (!response.data.cast || response.data.cast.length === 0) {
      console.error("출연 영화 정보가 없습니다.");
      return [];
    }

    // 중복 제거 (영화 ID 기준)
    const uniqueMovies = response.data.cast.filter(
      (movie, index, self) => index === self.findIndex((m) => m.id === movie.id)
    );

    // 인기순으로 정렬
    const sortedMovies = uniqueMovies.sort((a, b) => b.popularity - a.popularity);

    return sortedMovies; // 중복 제거 및 정렬된 영화 리스트 반환
  } catch (error) {
    console.error("Failed to fetch movies by actor:", error);
    throw new Error("배우의 출연 영화를 가져오는 데 실패했습니다.");
  }
};
