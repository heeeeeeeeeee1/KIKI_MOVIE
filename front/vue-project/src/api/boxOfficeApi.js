import axios from "axios";

const KOFIC_API_KEY = import.meta.env.VITE_KOFIC_API_KEY;
const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY;

const KOFIC_BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/";
const TMDB_BASE_URL = "https://api.themoviedb.org/3";

// 어제 날짜를 YYYYMMDD 형식으로 반환하는 함수
const getYesterdayDate = () => {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  
  const year = yesterday.getFullYear();
  const month = String(yesterday.getMonth() + 1).padStart(2, '0');
  const day = String(yesterday.getDate()).padStart(2, '0');
  
  return `${year}${month}${day}`;
};

// KOFIC API: 박스오피스 데이터 가져오기
export const getBoxOfficeData = async () => {
  const targetDt = getYesterdayDate();
  try {
    const response = await axios.get(`${KOFIC_BASE_URL}searchDailyBoxOfficeList.json`, {
      params: {
        key: KOFIC_API_KEY,
        targetDt,
      },
    });
    
    if (!response.data.boxOfficeResult) {
      throw new Error('박스오피스 데이터가 없습니다.');
    }
    
    return response.data.boxOfficeResult.dailyBoxOfficeList;
  } catch (error) {
    console.error("KOFIC 박스오피스 데이터를 가져오는 중 오류 발생:", error);
    if (error.response) {
      console.error("응답 상태:", error.response.status);
      console.error("응답 데이터:", error.response.data);
    }
    return [];
  }
};

// TMDB API: 영화 포스터 가져오기
export const getMoviePoster = async (movieTitle) => {
  try {
    const response = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
      params: {
        api_key: TMDB_API_KEY,
        query: movieTitle,
        language: 'ko-KR', // 한국어 결과 우선
      },
    });

    if (response.data.results.length > 0 && response.data.results[0].poster_path) {
      return `https://image.tmdb.org/t/p/w500${response.data.results[0].poster_path}`;
    }
    return "https://via.placeholder.com/150";
  } catch (error) {
    console.error(`TMDB 포스터 검색 중 오류 발생: ${movieTitle}`, error);
    if (error.response) {
      console.error("응답 상태:", error.response.status);
      console.error("응답 데이터:", error.response.data);
    }
    return "https://via.placeholder.com/150";
  }
};

// 박스오피스 + 포스터 데이터 조합
export const getBoxOfficeWithPosters = async () => {
  try {
    const boxOfficeData = await getBoxOfficeData();
    if (!boxOfficeData.length) {
      throw new Error('박스오피스 데이터를 가져올 수 없습니다.');
    }

    const boxOfficeWithPosters = await Promise.all(
      boxOfficeData.map(async (movie) => {
        const poster = await getMoviePoster(movie.movieNm);
        return {
          ...movie,
          poster,
        };
      })
    );

    return boxOfficeWithPosters;
  } catch (error) {
    console.error("데이터 조합 중 오류 발생:", error);
    return [];
  }
};

// 테스트를 위한 실행 코드
(async () => {
  try {
    const data = await getBoxOfficeWithPosters();
    console.log("Final Box Office Data with Posters:", data);
    console.log("데이터 개수:", data.length);
  } catch (error) {
    console.error("실행 중 오류 발생:", error);
  }
})();