<template>
  <div class="signup-main">
    <section class="signup-left">
      <div>
        <RouterLink :to="{ name: 'MainHomeView' }" class="logo-accounts">
          <div class="img-container">
            <img src="@/assets/kiki_logo.png" alt="키키무비 로고 이미지">
          </div>
        </RouterLink>
        <h1>
          당신의 데이터를 기반으로<br />
          개인 맞춤형 영화 추천을<br />
          경험해보세요
        </h1>
      </div>
    </section>
    <section class="signup-right">
      <div class="right__form">
        <h2>Sign Up</h2>
        <form @submit.prevent="signUp">
          <div class="form__input">
            <label for="email">이메일</label>
            <input type="email" id="email" v-model.trim="email" required />
          </div>
          <div class="form__input">
            <label for="username">닉네임</label>
            <input type="text" id="username" v-model.trim="username" required />
          </div>
          <div class="form__input">
            <label for="password1">비밀번호</label>
            <input
              type="password"
              id="password1"
              v-model.trim="password1"
              required
            />
          </div>
          <div class="form__input">
            <label for="password2">비밀번호 확인</label>
            <input
              type="password"
              id="password2"
              v-model.trim="password2"
              required
            />
          </div>
          <div class="form__input">
            <label for="gender">성별</label>
            <div class="input_gender">
              <input
                type="button"
                id="male"
                value="남성"
                :class="{ selected: gender === 'male' }"
                @click="gender = 'male'"
              />
              <input
                type="button"
                id="female"
                value="여성"
                :class="{ selected: gender === 'female' }"
                @click="gender = 'female'"
              />
            </div>
          </div>
          <div class="form__input">
            <label for="birth_date">태어난 년도</label>
            <input type="date" id="birth_date" v-model="birth_date" required />
          </div>
          <input type="submit" value="회원가입" />
        </form>
        <!-- <div class="divider">
          <span>OR</span>
        </div>
        <div class="social-login">
          <div class="social__google">
            <img src="@/assets/google.png" alt="google login" /><br />
          </div>
          <div class="social__kakao">
            <img src="@/assets/kakao.png" alt="kakao login" /><br />
          </div>
        </div> -->
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const gender = ref(null);
const email = ref(null);
const birth_date = ref(null);

const store = useCounterStore();
const router = useRouter();

const signUp = function () {
  if (!gender.value) {
    alert("성별을 선택해 주세요."); // 사용자에게 경고 메시지 표시
    return; // 폼 제출 중단
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    gender: gender.value === "male" ? "M" : "W",
    email: email.value,
    birth_date: birth_date.value,
  };
  store.signUp(payload);

  router.push({ name: "LogInView" });
};
</script>

<style scoped>
@import "@/assets/styles/components/signup.css";
</style>
