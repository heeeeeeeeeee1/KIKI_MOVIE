// src/stores/counter.js
import { ref, computed } from 'vue';
import { defineStore } from "pinia";
import axios from 'axios'
import { useRouter } from 'vue-router'


// export const useCounterStore = defineStore("counter", {
//   state: () => ({
//     count: 0,
//   }),
//   actions: {
//     increment() {
//       this.count++;
//     },
//     signUp(payload) {
//       console.log("Sign up payload from store:", payload);
//       // 회원가입 로직 추가
//     },
//   },
// });

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const username = ref('')
  const profileData = ref({ // profileData 초기화
    username: '',
    email: '',
    introduce: '',
    gender: '',
    birth_date: '',
  })

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
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
  // const signUp = function (payload) {
  //   const { username, password1, password2, email, introduce, gender, birth_date } = payload

  //   axios({
  //     method: 'post',
  //     url: `${API_URL}/accounts/signup/`,
  //     data: {
  //       username, password1, password2, email, introduce, gender, birth_date,
  //     }
  //   })
  //     .then((res) => {
  //       console.log("응답데이터", res.data)
  //       // console.log('회원가입 성공')
  //       const password = password1
  //       logIn({ username, password })
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  // }

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
const fetchUserProfile = () => {
  return axios({
    method: 'get',
    url: `${API_URL}/accounts/myprofile/`,
    headers: {
      Authorization: `Token ${token.value}`,
    },
  })
    .then((res) => {
      if (res.data) {
        profileData.value = {
          username: res.data.username || '',
          email: res.data.email || '',
          gender: res.data.gender || '',
          birth_date: res.data.birth_date || '',
          introduce: res.data.introduce || '',
        };
        console.log('프로필 데이터: ', profileData.value)
        return profileData.value; // 프로필 데이터 반환
      } else {
        console.error('API 응답이 비어 있습니다.');
        throw new Error('Empty response');
      }
    })
    .catch((err) => {
      console.error('프로필 정보 불러오기 실패:', err);
      profileData.value = {
        username: '',
        email: '',
        gender: '',
        birth_date: '',
        introduce: '',
      };
      throw err;
    });
};

  
  // 사용자 프로필 정보 업데이트
  const updateUserInfo = (updatedData) => {
    return axios({
      method: 'patch',
      url: `${API_URL}/accounts/user/`,
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
    });
  };

  
  // [추가기능] 로그아웃
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
  return { API_URL, signUp, logIn, token, isLogin, fetchUserInfo, fetchUserProfile, updateUserInfo, profileData, username, logOut }
}, { persist: true })
