import axios from "axios";

const KOFIC_API_KEY = "";
const TMDB_API_KEY = "";

const KOFIC_BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/";
const TMDB_BASE_URL = "https://api.themoviedb.org/3";

// KOFIC API: 박스오피스 데이터 가져오기
export const getBoxOfficeData = async () => {
  const today = new Date();
  const targetDt = today.toISOString().split("T")[0].replace(/-/g, ""); // YYYYMMDD 형식
  try {
    const response = await axios.get(`${KOFIC_BASE_URL}searchDailyBoxOfficeList.json`, {
      params: {
        key: KOFIC_API_KEY,
        targetDt,
      },
    });
    return response.data.boxOfficeResult.dailyBoxOfficeList;
  } catch (error) {
    console.error("KOFIC 박스오피스 데이터를 가져오는 중 오류 발생:", error);
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
      },
    });

    if (response.data.results.length > 0) {
      return `https://image.tmdb.org/t/p/w500${response.data.results[0].poster_path}`;
    }
    return "https://via.placeholder.com/150"; // 포스터가 없는 경우 기본 이미지
  } catch (error) {
    console.error(`TMDB 포스터 검색 중 오류 발생: ${movieTitle}`, error);
    return "https://via.placeholder.com/150";
  }
};

// 박스오피스 + 포스터 데이터 조합
export const getBoxOfficeWithPosters = async () => {
  const boxOfficeData = await getBoxOfficeData();

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
};
