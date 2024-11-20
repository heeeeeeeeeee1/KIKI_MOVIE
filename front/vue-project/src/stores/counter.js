// src/stores/counter.js
import { defineStore } from "pinia";

export const useCounterStore = defineStore("counter", {
  state: () => ({
    count: 0,
  }),
  actions: {
    increment() {
      this.count++;
    },
    signUp(payload) {
      console.log("Sign up payload from store:", payload);
      // 회원가입 로직 추가
    },
  },
});
