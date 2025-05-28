import axios from "axios";

const KOFIC_API_KEY = import.meta.env.VITE_KOFIC_API_KEY;
const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY;

const KOFIC_BASE_URL = "https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/";
const TMDB_BASE_URL = "https://api.themoviedb.org/3";

// 숫자 변환을 위한 매핑 테이블
const romanToArabic = {
  'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
  'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
};

const arabicToRoman = {
  1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
  6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X'
};

// 숫자 형식 변환 유틸리티 함수
const convertNumberFormat = (title) => {
  // 로마 숫자를 아라비아 숫자로
  let arabicVersion = title;
  Object.entries(romanToArabic).forEach(([roman, arabic]) => {
    arabicVersion = arabicVersion.replace(new RegExp(` ${roman}(?!\\w)`, 'g'), ` ${arabic}`);
  });

  // 아라비아 숫자를 로마 숫자로
  let romanVersion = title;
  Object.entries(arabicToRoman).forEach(([arabic, roman]) => {
    romanVersion = romanVersion.replace(new RegExp(` ${arabic}(?!\\w)`, 'g'), ` ${roman}`);
  });

  return [title, arabicVersion, romanVersion];
};

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
const getBoxOfficeData = async () => {
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

// TMDB API에서 영화 상세 정보 가져오기
const getMovieDetailsFromTMDB = async (movieTitle, originalTitle = '') => {
  try {
    // 제목의 다양한 형식 생성
    const titleVariations = convertNumberFormat(movieTitle);
    const originalTitleVariations = originalTitle ? convertNumberFormat(originalTitle) : [];
    let searchResponse = null;

    // 1차: 한글 제목의 모든 변형으로 시도
    for (const title of titleVariations) {
      try {
        searchResponse = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
          params: {
            api_key: TMDB_API_KEY,
            query: title,
            language: 'ko-KR',
          },
        });
        if (searchResponse.data.results.length > 0) break;
      } catch (error) {
        console.log(`"${title}" 검색 실패, 다음 변형 시도`);
      }
    }

    // 2차: 영어 제목의 모든 변형으로 시도
    if ((!searchResponse || searchResponse.data.results.length === 0) && originalTitle) {
      for (const title of originalTitleVariations) {
        try {
          console.log(`영어 제목 변형 시도: "${title}"`);
          searchResponse = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
            params: {
              api_key: TMDB_API_KEY,
              query: title,
              language: 'ko-KR',
            },
          });
          if (searchResponse.data.results.length > 0) break;
        } catch (error) {
          console.log(`"${title}" 검색 실패, 다음 변형 시도`);
        }
      }
    }

    if (!searchResponse || searchResponse.data.results.length === 0) {
      throw new Error('영화를 찾을 수 없습니다.');
    }

    const movie = searchResponse.data.results[0];
    
    // 영화 상세 정보 가져오기
    const detailsResponse = await axios.get(`${TMDB_BASE_URL}/movie/${movie.id}`, {
      params: {
        api_key: TMDB_API_KEY,
        language: 'ko-KR',
      },
    });

    // 영화 크레딧 정보 가져오기 (배우, 감독)
    const creditsResponse = await axios.get(`${TMDB_BASE_URL}/movie/${movie.id}/credits`, {
      params: {
        api_key: TMDB_API_KEY,
        language: 'ko-KR',
      },
    });

    const director = creditsResponse.data.crew.find(person => person.job === 'Director');
    const cast = creditsResponse.data.cast.slice(0, 5);

    return {
      tmdbId: movie.id,
      title: detailsResponse.data.title,
      originalTitle: detailsResponse.data.original_title,
      overview: detailsResponse.data.overview,
      genres: detailsResponse.data.genres.map(genre => genre.name).join(', '),
      releaseDate: detailsResponse.data.release_date,
      posterPath: detailsResponse.data.poster_path 
        ? `https://image.tmdb.org/t/p/w500${detailsResponse.data.poster_path}`
        : "https://via.placeholder.com/500x750",
      voteAverage: detailsResponse.data.vote_average,
      runtime: detailsResponse.data.runtime,
      director: director ? director.name : '정보 없음',
      cast: cast.map(actor => ({
        name: actor.name,
        character: actor.character,
        profilePath: actor.profile_path 
          ? `https://image.tmdb.org/t/p/w200${actor.profile_path}`
          : null
      }))
    };
  } catch (error) {
    console.error(`TMDB 영화 상세 정보 검색 중 오류 발생: ${movieTitle}`, error);
    throw error;
  }
};

// 박스오피스 데이터와 TMDB 상세 정보를 통합
export const getBoxOfficeWithDetails = async () => {
  try {
    const boxOfficeData = await getBoxOfficeData();
    if (!boxOfficeData.length) {
      throw new Error('박스오피스 데이터를 가져올 수 없습니다.');
    }

    const boxOfficeWithDetails = await Promise.all(
      boxOfficeData.map(async (movie) => {
        try {
          // 영화 제목과 영어 제목을 함께 전달
          const tmdbDetails = await getMovieDetailsFromTMDB(
            movie.movieNm, 
            movie.movieNmEn
          );
          return {
            ...movie,
            tmdbDetails,
          };
        } catch (error) {
          console.error(`영화 정보 검색 실패: ${movie.movieNm}`, error);
          // 검색 실패한 영화의 경우 기본 정보만 반환
          return {
            ...movie,
            tmdbDetails: {
              title: movie.movieNm,
              posterPath: "https://via.placeholder.com/500x750",
              overview: "상세 정보를 불러올 수 없습니다.",
              genres: "",
              releaseDate: movie.openDt,
            }
          };
        }
      })
    );

    return boxOfficeWithDetails;
  } catch (error) {
    console.error("데이터 조합 중 오류 발생:", error);
    return [];
  }
};

// 영화 포스터 URL 생성 유틸리티 함수
export const getTMDBImageUrl = (path, size = 'w500') => {
  if (!path) return "https://via.placeholder.com/500x750";
  return `https://image.tmdb.org/t/p/${size}${path}`;
};
