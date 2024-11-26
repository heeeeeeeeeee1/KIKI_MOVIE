import axios from "axios";
import { ref } from "vue";

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const BASE_URL = "https://api.themoviedb.org/3";

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
          language: "ko-KR",
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

export const getPopularActors = async (page = 1) => {
  try {
    const response = await axios.get(`${BASE_URL}/person/popular`, {
      params: { 
        api_key: TMDB_API_KEY, 
        page,
        language: "ko-KR",
      },
    });
    return response.data.results;
  } catch (error) {
    console.error("Failed to fetch popular actors:", error);
    throw new Error("인기 배우 정보를 가져오는 데 실패했습니다.");
  }
};

export const getMoviesByActor = async (actorId) => {
  try {
    const response = await axios.get(`${BASE_URL}/person/${actorId}/movie_credits`, {
      params: {
        api_key: TMDB_API_KEY,
        language: "ko-KR",
      },
    });

    console.log("TMDB API 응답 데이터:", response.data.cast);

    if (!response.data.cast || response.data.cast.length === 0) {
      console.error("출연 영화 정보가 없습니다.");
      return [];
    }

    const uniqueMovies = response.data.cast.filter(
      (movie, index, self) => index === self.findIndex((m) => m.id === movie.id)
    );

    const sortedMovies = uniqueMovies
      .sort((a, b) => b.popularity - a.popularity)
      .slice(0, 5);  // 상위 5개 영화만 선택

    return sortedMovies;
  } catch (error) {
    console.error("Failed to fetch movies by actor:", error);
    throw new Error("배우의 출연 영화를 가져오는 데 실패했습니다.");
  }
};