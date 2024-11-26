import axios from "axios";

// 환경 변수에서 API 키 가져오기
const NAVER_CLIENT_ID = import.meta.env.VITE_NAVER_CLIENT_ID;
const NAVER_CLIENT_SECRET = import.meta.env.VITE_NAVER_CLIENT_SECRET;

export const fetchMoviesByActor = async (actorName) => {
  try {
    console.log("네이버 API 호출 시작:", actorName);
    const response = await axios.get("https://openapi.naver.com/v1/search/movie.json", {
      headers: {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
      },
      params: {
        query: encodeURIComponent(actorName), // 배우 이름 URL 인코딩
        display: 10, // 최대 10개의 결과 가져오기
      },
    });

    console.log("네이버 API 응답:", response.data);

    // 결과에서 영화 제목과 링크만 반환
    return response.data.items.map((movie) => ({
      title: movie.title.replace(/<[^>]+>/g, ""), // HTML 태그 제거
      link: movie.link,
    }));
  } catch (error) {
    console.error("네이버 영화 검색 API 호출 오류:", error.response?.data || error.message);
    throw new Error("영화 정보를 가져올 수 없습니다.");
  }
};
