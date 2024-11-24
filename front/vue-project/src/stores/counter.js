// src/stores/counter.js
import { ref, computed } from 'vue';
import { defineStore } from "pinia";
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const username = ref('')

  // 사용자 데이터 저장
  const profileData = ref({
    username: '',
    email: '',
    introduce: '',
    gender: '',
    birth_date: '',
  })

  // 작성한 리뷰와 보고싶어요 영화
  const watchedReviews = ref([]); // 사용자가 작성한 리뷰 목록
  const wishlistMovies = ref([]); // 사용자가 보고싶어요를 누른 영화 목록

  const isLogin = computed(() => token.value !== null);
  const router = useRouter()

  // 회원가입 요청 액션
  const signUp = function (payload) {
    const { username, password1, password2, email, introduce, gender, birth_date } = payload
  
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, 
        password1, 
        password2, 
        email, 
        introduce, 
        gender, 
        birth_date
      }
    })
    .then((res) => {
      console.log('회원가입 성공');
      const password = password1;
      logIn({ username, password });
    })
    .catch((error) => {
      if (error.response) {
        // 서버가 응답한 오류
        console.error('서버 응답 오류:', error.response.data);
        console.error('상태 코드:', error.response.status);
        alert(error.response.data.detail || '회원가입 중 오류가 발생했습니다.');
      } else if (error.request) {
        // 요청은 보냈지만 응답을 받지 못한 경우
        console.error('서버 응답 없음:', error.request);
        alert('서버와 통신할 수 없습니다.');
      } else {
        // 요청 설정 중 오류 발생
        console.error('요청 설정 오류:', error.message);
        alert('요청 중 오류가 발생했습니다.');
      }
    });
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload
    console.log("로그인 요청 데이터:", payload); // 요청 데이터 디버깅

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        router.push({ name: 'MainHomeView' })
        // console.log(res.data)
        console.log('로그인 성공')
      })
      .catch((error) => {
        if (error.response) {
          console.error("로그인 실패:", error.response.data); // 전체 응답 데이터 출력
          alert(error.response.data.non_field_errors?.[0] || '로그인 중 오류가 발생했습니다.');
        }
      });
  
  }
  
  // 사용자 이름 가져오기 (nav 컴포넌트에서 활용)
  const fetchUserInfo = () => {
    return axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((res) => {
        // console.log('res: ', res)
        username.value = res.data.username; // username 업데이트
        // console.log('fetchUserInfo에서 username 업데이트:', username.value);
        // return res.data; // Promise 반환
      })
      .catch((err) => {
        console.log('사용자 정보 불러오기 실패:', err)
        token.value = null; // 인증 실패 시 로그아웃 처리
        throw err
      });
  };
  

// 사용자 프로필 정보 가져오기
const fetchUserProfile = async () => {
  try {
    const response = await axios({
      method: 'get',
      url: `${API_URL}/accounts/myprofile/`,
      headers: { Authorization: `Token ${token.value}` },
    });

    if (response.data) {
      // 프로필 데이터 업데이트
      profileData.value = {
        username: response.data.user_info.username || '',
        email: response.data.user_info.email || '',
        gender: response.data.user_info.gender || '',
        birth_date: response.data.user_info.birth_date || '',
        introduce: response.data.user_info.introduce || '자기 소개가 없습니다.',
      };

      // 리뷰와 위시리스트 데이터 업데이트
      watchedReviews.value = response.data.watched_reviews || [];
      wishlistMovies.value = response.data.wishlist || [];

      return {
        profileData: profileData.value,
        watchedReviews: watchedReviews.value,
        wishlistMovies: wishlistMovies.value
      };
    }
    throw new Error('데이터가 없습니다.');
  } catch (err) {
    console.error('프로필 정보 불러오기 실패:', err);
    // 기본값으로 초기화
    profileData.value = {
      username: '',
      email: '',
      gender: '',
      birth_date: '',
      introduce: '자기 소개가 없습니다.',
    };
    watchedReviews.value = [];
    wishlistMovies.value = [];
    throw err;
  }
};


  // 사용자 프로필 정보 수정
  const updateUserInfo = (updatedData) => {
    return axios({
      method: 'patch',
      url: `${API_URL}/accounts/myprofile/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: updatedData,
    })
    .then((res) => {
      console.log('사용자 정보 업데이트 성공:', res.data);
      profileData.value = { ...profileData.value, ...res.data };
      return res.data
    })
    .catch((err) => {
      console.log('사용자 정보 업데이트 실패:', err);
      throw err;
    });
  };

  // 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        username.value = '';
        // router.push({ name: 'MainHomeView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    API_URL,
    token,
    username,
    isLogin,
    profileData,
    signUp,
    logIn,
    logOut,
    fetchUserInfo,
    profileData,
    watchedReviews,
    wishlistMovies,
    fetchUserProfile,
    updateUserInfo,
  }
}, { persist: true })
