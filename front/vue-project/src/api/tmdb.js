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
      // 1. 기본 영화 목록 가져오기
      const response = await axios.get(`${BASE_URL}/movie/popular`, {
        params: {
          api_key: TMDB_API_KEY,
          page,
          language: "ko-KR",
        },
      });
  
      // 2. 각 영화의 상세 정보와 크레딧 정보 가져오기
      const moviesWithDetails = await Promise.all(
        response.data.results.map(async (movie) => {
          // 크레딧 정보 가져오기 (배우, 감독)
          const creditResponse = await axios.get(`${BASE_URL}/movie/${movie.id}/credits`, {
            params: {
              api_key: TMDB_API_KEY,
              language: "ko-KR",
            },
          });
  
          const actors = creditResponse.data.cast
            ?.slice(0, 5)  // 상위 5명의 배우만
            .map(actor => ({
              id: actor.id,
              name: actor.name,
              profile_path: actor.profile_path,
              character: actor.character
            })) || [];
  
          const directors = creditResponse.data.crew
            ?.filter(person => person.job === 'Director')
            .map(director => ({
              id: director.id,
              name: director.name,
              profile_path: director.profile_path
            })) || [];
  
          return {
            ...movie,
            adult: checkAdultContent(movie),
            genres: convertGenreIdsToNames(movie.genre_ids),
            actors: actors,
            directors: directors
          };
        })
      );
  
      movies.value = moviesWithDetails;
  
      console.log("영화 데이터 로드 완료. 첫 번째 영화:", movies.value[0]);
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

const searchActor = async (actorName) => {
  try {
    console.group(`배우 검색: "${actorName}"`);

    const response = await axios.get(`${BASE_URL}/search/person`, {
      params: {
        api_key: TMDB_API_KEY,
        query: actorName,
        language: "ko-KR",
        include_adult: false,
      },
    });

    if (!response.data.results || response.data.results.length === 0) {
      console.warn(`배우 "${actorName}" 검색 결과 없음`);
      console.groupEnd();
      throw new Error(`배우 "${actorName}"를 찾을 수 없습니다.`);
    }

    const actor = response.data.results[0];
    console.log("검색된 배우 정보:", {
      id: actor.id,
      name: actor.name,
      known_for_department: actor.known_for_department,
      popularity: actor.popularity,
    });

    console.groupEnd();
    return actor.id;
  } catch (error) {
    console.error("배우 검색 실패:", error);
    console.groupEnd();
    throw new Error("배우 검색에 실패했습니다.");
  }
};

export const getMoviesByActor = async (actorNameOrId) => {
  console.group(`영화 검색 시작: ${actorNameOrId}`);
  let actorId = actorNameOrId;
  let actorName = typeof actorNameOrId === "string" ? actorNameOrId : null;

  // actorNameOrId가 숫자가 아니면 배우 이름으로 간주하고 검색
  if (isNaN(actorNameOrId)) {
    try {
      actorId = await searchActor(actorNameOrId);
      console.log(`배우 이름 "${actorNameOrId}"의 TMDB ID: ${actorId}`);
    } catch (error) {
      console.error("배우 검색 실패:", error);
      console.groupEnd();
      return [];
    }
  } else {
    // ID로 배우 정보 가져오기
    try {
      const actorResponse = await axios.get(`${BASE_URL}/person/${actorId}`, {
        params: {
          api_key: TMDB_API_KEY,
          language: "ko-KR",
        },
      });
      actorName = actorResponse.data.name;
      console.log(`TMDB ID ${actorId}의 배우 이름: ${actorName}`);
    } catch (error) {
      console.error("배우 정보 가져오기 실패:", error);
    }
  }

  try {
    console.log(`필모그래피 검색 시작 - ID: ${actorId}, 이름: ${actorName}`);

    const response = await axios.get(
      `${BASE_URL}/person/${actorId}/movie_credits`,
      {
        params: {
          api_key: TMDB_API_KEY,
          language: "ko-KR",
        },
      }
    );

    if (!response.data.cast || response.data.cast.length === 0) {
      console.warn("출연 영화 정보가 없습니다.");
      console.groupEnd();
      return [];
    }

    console.log(`전체 출연작 수: ${response.data.cast.length}`);

    // 중복 제거 및 필터링
    const uniqueMovies = response.data.cast
      .filter(
        (movie, index, self) =>
          index === self.findIndex((m) => m.id === movie.id) &&
          movie.release_date && // 개봉일이 있는 영화만
          movie.title // 제목이 있는 영화만
      )
      .sort((a, b) => {
        // 1. 개봉일 기준 최신순
        const dateA = new Date(a.release_date || "1900-01-01");
        const dateB = new Date(b.release_date || "1900-01-01");
        return dateB - dateA;
      })
      .slice(0, 10); // 최신 영화 10개만 선택

    console.log(`필터링 후 영화 수: ${uniqueMovies.length}`);
    console.log(
      "선택된 영화 목록:",
      uniqueMovies.map((movie) => ({
        id: movie.id,
        title: movie.title,
        release_date: movie.release_date,
      }))
    );

    // 필요한 정보만 매핑
    const result = uniqueMovies.map((movie) => ({
      id: movie.id,
      title: movie.title,
      release_date: movie.release_date,
      character: movie.character,
      poster_path: movie.poster_path,
      overview: movie.overview,
    }));

    console.groupEnd();
    return result;
  } catch (error) {
    console.error("영화 정보 가져오기 실패:", error);
    console.groupEnd();
    throw new Error("배우의 출연 영화를 가져오는 데 실패했습니다.");
  }
};
