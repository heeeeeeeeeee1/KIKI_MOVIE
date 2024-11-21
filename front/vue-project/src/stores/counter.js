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
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        router.push({ name: 'MainHomeView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }
  return { API_URL, signUp, logIn, token, isLogin, logOut }
}, { persist: true })
