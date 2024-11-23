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
  const username = ref('');
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
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload

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
        // console.log('로그인 성공')
      })
      .catch((err) => {
        console.log(err)
      })
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
        console.log('사용자 정보 불러오기 실패:', err);
        token.value = null; // 인증 실패 시 로그아웃 처리
        throw err;
      });
  };
  

  // 사용자 프로필 정보 가져오기
  const fetchUserProfile = () => {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((res) => {
        profileData.value = res.data; // 사용자 프로필 정보 저장
      })
      .catch((err) => {
        console.log('프로필 정보 불러오기 실패:', err);
      });
  };
  
  // 사용자 프로필 정보 업데이트
  const updateUserInfo = (updatedData) => {
    axios({
      method: 'patch',
      url: `${API_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: updatedData,
    })
      .then((res) => {
        console.log('사용자 정보 업데이트 성공:', res.data);
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
  return { API_URL, signUp, logIn, token, isLogin, fetchUserInfo, username, logOut }
}, { persist: true })
