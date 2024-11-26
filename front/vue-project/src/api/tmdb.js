import axios from "axios";
import { ref } from "vue";

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const BASE_URL = "https://api.themoviedb.org/3";

// 장르 저장을 위한 ref 생성
const genreMap = ref({});

// 장르 목록을 가져오는 함수
const fetchGenres = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/genre/movie/list`, {
      params: {
        api_key: TMDB_API_KEY,
        language: "ko-KR",
      },
    });

    // 장르 ID와 이름을 매핑
    const genres = response.data.genres;
    const genreMapping = {};
    genres.forEach((genre) => {
      genreMapping[genre.id] = genre.name;
    });

    genreMap.value = genreMapping;
    console.log("장르 목록 로드 완료:", genreMap.value);
  } catch (error) {
    console.error("장르 목록 가져오기 실패:", error);
  }
};

// genre_ids를 문자열로 변환하는 함수
const convertGenreIdsToNames = (genreIds) => {
  if (!genreIds) return [];
  return genreIds.map((id) => genreMap.value[id] || "기타").filter(Boolean);
};

// 성인 콘텐츠 체크 함수
const checkAdultContent = (movie) => {
  console.group(`성인 콘텐츠 체크: ${movie.title}`);

  // 기존 TMDB adult 플래그
  if (movie.adult) {
    console.log("TMDB adult 플래그: true");
    console.groupEnd();
    return true;
  }

  // 성인 콘텐츠 관련 키워드
  // 성인 콘텐츠 관련 키워드
  const adultKeywords = [
    // 직접적인 성인 콘텐츠 표현
    "에로",
    "섹스",
    "성인",
    "adult",
    "erotic",
    "nude",
    "누드",
    "19금",
    "18금",
    "청불",
    "r-rated",
    "x-rated",

    // 간접적 성인 콘텐츠 표현
    "첫경험",
    "첫날밤",
    "호스티스",
    "스트리퍼",
    "마사지",
    "욕망",
    "유혹",
    "정사",
    "불륜",

    // 영어 키워드
    "sex",
    "adult",
    "erotic",
    "nude",
    "stripper",
    "hostess",
    "desire",
    "lust",
    "affair",
    "uncensored",
    "restricted",
    "sensual",
    "passionate",
    "forbidden",

    // 기타 관련 키워드
    "연애지침서",
    "운명의밤",
    "나이트",
    "풀사롱",
    "안마",
    "연상연하",
    "원나잇",
    "one night",
    "야한",
    "야동",
    "베드신",
    "bed scene",
    "노출",
    "exposure",
    "관계",
    "은밀한",
    "심야",
    "midnight",
    "자극",
    "자극적",
    "도발",
    "도발적",
    "감금",
    "금지",
    "미혼",
    "미망인",
    "과부",
    "신체",
    "신체접촉",
    "육체",
    "탐닉",
    "탐험",
    "탐색",
    "관계",
    "충동",

    // 특수문자를 포함한 변형
    "19+",
    "18+",
    "r+",
    "x+",
    "청소년관람불가",
    "청관불",
    "미성년자관람불가",
    "미성년자시청불가",

    // 한자 포함 키워드
    "성인용",
    "성인물",
    "성인영화",
    "성인등급",

    // 속어 및 은어
    "야릇",
    "야릇한",
    "야릇해",
    "야릇하게",
    "은밀",
    "은밀한",
    "은밀하게",
    "몰래",

    // 장르 관련
    "에로물",
    "에로틱",
    "에로스",
    "에로티카",
    "섹시",
    "sexy",
    "성적",
    "sexual",
  ];

  // 제목에서 키워드 체크 (원제목 포함)
  const foundTitleKeyword = adultKeywords.find(
    (keyword) =>
      movie.title?.toLowerCase().includes(keyword) ||
      movie.original_title?.toLowerCase().includes(keyword)
  );

  if (foundTitleKeyword) {
    console.log(`제목에서 성인 키워드 발견: "${foundTitleKeyword}"`);
    console.log(`- 한글제목: ${movie.title}`);
    console.log(`- 원제목: ${movie.original_title}`);
    console.groupEnd();
    return true;
  }

  // 설명에서 키워드 체크
  const foundOverviewKeyword = adultKeywords.find((keyword) =>
    movie.overview?.toLowerCase().includes(keyword)
  );

  if (foundOverviewKeyword) {
    console.log(`설명에서 성인 키워드 발견: "${foundOverviewKeyword}"`);
    console.log(`- 설명 내용: ${movie.overview}`);
    console.groupEnd();
    return true;
  }

  // 평점 기반 체크 (예: 특정 평점 이상인 경우)
  if (movie.vote_average >= 8 && movie.adult) {
    console.log(`높은 평점과 adult 플래그: ${movie.vote_average}`);
    console.groupEnd();
    return true;
  }

  console.log("성인 콘텐츠 아님");
  console.groupEnd();
  return false;
};

// 인기 영화 정보 가져오기
export function useTmdb() {
  const movies = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const fetchPopularMovies = async (page = 1) => {
    // 장르 데이터가 없으면 먼저 가져오기
    if (Object.keys(genreMap.value).length === 0) {
      await fetchGenres();
    }

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

      // 성인 콘텐츠 체크를 포함하여 데이터 매핑
      movies.value = response.data.results.map((movie) => ({
        ...movie,
        adult: checkAdultContent(movie),
        genres: convertGenreIdsToNames(movie.genre_ids),
      }));

      console.log(
        "영화 데이터 로드 완료. 첫 번째 영화의 장르:",
        movies.value[0]?.genre_ids,
        "->",
        movies.value[0]?.genres
      );
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
  // 장르 데이터가 없으면 먼저 가져오기
  if (Object.keys(genreMap.value).length === 0) {
    await fetchGenres();
  }

  try {
    const response = await axios.get(
      `${BASE_URL}/person/${actorId}/movie_credits`,
      {
        params: {
          api_key: TMDB_API_KEY,
          language: "ko-KR", // 언어를 한국어로 설정
        },
      }
    );

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
    // 인기순으로 정렬
    //const sortedMovies = uniqueMovies.sort(
    //  (a, b) => b.popularity - a.popularity
    //);

    // 성인 콘텐츠 체크와 장르 정보를 포함하여 데이터 매핑
    const moviesWithAdultCheck = sortedMovies.map((movie) => ({
      ...movie,
      adult: checkAdultContent(movie),
      genres: convertGenreIdsToNames(movie.genre_ids),
    }));

    return moviesWithAdultCheck;
  } catch (error) {
    console.error("Failed to fetch movies by actor:", error);
    throw new Error("배우의 출연 영화를 가져오는 데 실패했습니다.");
  }
};