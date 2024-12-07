import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from 'vue-router';

export const useMovieStore = defineStore("movieStore", () => {
  const API_URL = "http://127.0.0.1:8000";
  const counterStore = useCounterStore();
  const router = useRouter();
  const token = computed(() => counterStore.token);

  const movie = ref({});
  const movies = ref([]);
  const reviews = ref([]);
  const singleReview = ref(null);
  const isLoading = ref(false);
  const allReviews = ref([]);
  const latestUserReview = ref(null);

  // TMDB 영화를 Django DB에 저장하거나 조회하는 함수
  const createOrGetMovie = async (movieData) => {
    try {
      const response = await axios.get(`${API_URL}/movies/tmdb/${movieData.id}/`);
      console.log('기존 영화 찾음:', response.data);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        try {
          // 1. 기본 영화 정보 생성
          const createData = {
            id: movieData.id,
            tmdb_id: movieData.id,
            title: movieData.title || '',
            original_title: movieData.original_title || '',
            description: movieData.overview || '',
            poster_path: movieData.poster_path || '',
            release_date: movieData.release_date || '',
            vote_average: movieData.vote_average || 0,
            popularity: movieData.popularity || 0,
            video_path: '',
            runtime: '0',
            status: 'Released',
            tagline: '',
            adult: movieData.adult || false,
            created_at: new Date().toISOString().split('T')[0]
          };
  
          console.log('생성할 영화 데이터:', createData);
          const createResponse = await axios.post(`${API_URL}/movies/tmdb/`, createData);
          const movieId = createResponse.data.id;
  
          // 2. 추가 정보 병렬로 처리
          await Promise.all([
            // 장르 추가
            movieData.genres?.length > 0 &&
              axios.post(`${API_URL}/movies/${movieId}/genres/`, {
                genres: movieData.genres.map(genre => genre.name || genre)
              }).catch(e => console.error('장르 추가 실패:', e)),
  
            // 배우 추가
            movieData.actors?.length > 0 &&
              axios.post(`${API_URL}/movies/${movieId}/actors/`, {
                actors: movieData.actors
              }).catch(e => console.error('배우 추가 실패:', e)),
  
            // 감독 추가
            movieData.directors?.length > 0 &&
              axios.post(`${API_URL}/movies/${movieId}/directors/`, {
                directors: movieData.directors
              }).catch(e => console.error('감독 추가 실패:', e))
          ]);
  
          // 3. 최종 영화 정보 조회하여 반환
          const finalResponse = await axios.get(`${API_URL}/movies/${movieId}/detail/`);
          return finalResponse.data;
  
        } catch (createError) {
          console.error('영화 생성 오류:', createError);
          throw createError;
        }
      }
      throw error;
    }
  };

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
    if (!token.value) {
      router.push("/login");
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "post",
      url: `${API_URL}/movies/${moviePk}/wishlist/`,
      headers: { Authorization: `Token ${token.value}` },
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
    if (!token.value) {
      alert("로그인이 필요합니다.");
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "post",
      url: `${API_URL}/movies/reviews/${reviewPk}/like/`,
      headers: { Authorization: `Token ${token.value}` },
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
    if (!token.value) {
      console.error("유효한 토큰이 없습니다. 로그인이 필요합니다.");
      return Promise.reject("로그인이 필요합니다.");
    }
    return axios({
      method: "post",
      url: `${API_URL}/movies/${moviePk}/review/create/`,
      data: { content, score },
      headers: { Authorization: `Token ${token.value}` },
    })
    .then((res) => {
      console.log("작성된 리뷰 데이터:", res.data);
      return fetchMovieReviews(moviePk);
    })
    .catch((err) => {
      console.error("리뷰 작성 실패:", err.response?.data || err.message);
      throw err;
    });
  };

  const updateReview = function (reviewPk, data) {
    if (!token.value) {
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "put",
      url: `${API_URL}/movies/reviews/${reviewPk}/`,
      data: data,
      headers: { Authorization: `Token ${token.value}` }
    })
    .then((res) => {
      console.log("리뷰 수정 성공:", res.data);
      return res.data;
    })
    .catch((err) => {
      console.error("리뷰 수정 실패:", err.response?.data || err.message);
      throw err;
    });
  };
  
  const deleteReview = function (reviewPk) {
    if (!token.value) {
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "delete",
      url: `${API_URL}/movies/reviews/${reviewPk}/`,
      headers: { Authorization: `Token ${token.value}` }
    });
  };

  // 댓글 생성(로그인O)
  const createComment = function (reviewPk, content) {
    if (!token.value) {
      return Promise.reject("로그인이 필요합니다.");
    }
    
    return axios({
      method: "post",
      url: `${API_URL}/movies/reviews/${reviewPk}/comments/`,
      data: { content },
      headers: { Authorization: `Token ${token.value}` }
    });
  };

  const updateComment = function (commentId, content) {
    if (!token.value) {
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "put",
      url: `${API_URL}/movies/reviews/comments/${commentId}/`,
      data: { content },
      headers: { Authorization: `Token ${token.value}` }
    });
  };
  
  const deleteComment = function (commentId) {
    if (!token.value) {
      return Promise.reject("로그인이 필요합니다.");
    }
  
    return axios({
      method: "delete",
      url: `${API_URL}/movies/reviews/comments/${commentId}/`,
      headers: { Authorization: `Token ${token.value}` }
    });
  };

  // 모든 리뷰 데이터 가져오기
  const fetchAllReviews = async () => {
    isLoading.value = true;
    try {
      const response = await axios.get(`${API_URL}/movies/reviews/all/`);
      allReviews.value = response.data;
    } catch (error) {
      console.error('리뷰 데이터 로딩 실패:', error);
      allReviews.value = [];
    } finally {
      isLoading.value = false;
    }
  };
  
  const fetchLatestUserReview = async (username) => {
    try {
      const response = await axios.get(`${API_URL}/movies/reviews/latest/${username}/`);
      latestUserReview.value = response.data;
    } catch (error) {
      console.error('최신 리뷰 로딩 실패:', error);
      latestUserReview.value = null;
    }
  };

  return {
    movie,
    movies,
    reviews,
    singleReview,
    API_URL,
    allReviews,
    latestUserReview,
    getMovie,
    fetchMovieReviews,
    toggleLikeReview,
    getSingleReview,
    updateReview,
    deleteReview,
    createReview,
    createComment,
    updateComment,
    deleteComment,
    toggleWishlist,
    createOrGetMovie,
    fetchAllReviews,
    fetchLatestUserReview,
  };
});