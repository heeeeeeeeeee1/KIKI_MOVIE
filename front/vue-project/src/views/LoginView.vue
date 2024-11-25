<template>
  <main class="login-main">
    <RouterLink :to="{ name: 'MainHomeView' }"> 로고 </RouterLink>
    <section>
      <div class="login-container">
        <h1>LogIn</h1>
        <form @submit.prevent="logIn">
          <div class="form__input">
            <label for="username">유저 ID</label>
            <input
              type="text"
              id="username"
              v-model.trim="username"
              placeholder="유저 이름을 입력해주세요"
            /><br />
          </div>
          <div class="form__input">
            <label for="password">비밀번호</label>
            <input
              type="password"
              id="password"
              v-model.trim="password"
              placeholder="8자 이상 입력해주세요 (문자/숫자/기호 사용 기능)"
            /><br />
          </div>
          <input type="submit" value="로그인" />
        </form>
        <div class="password_signup">
          <a href="" class="find-password_btn">비밀번호를 잃어버리셨나요?</a>
          <div>
            <span class="signup_label">계정이 없으신가요?</span>
            <router-link to="/signup">회원가입</router-link>
          </div>
        </div>
        <div class="divider">
          <span>OR</span>
        </div>
        <div class="social-login">
          <div class="social__google">
            <img src="@/assets/google.png" alt="google login" /><br />
          </div>
          <div class="social__kakao">
            <img src="@/assets/kakao.png" alt="kakao login" /><br />
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";

const username = ref(null);
const password = ref(null);

const store = useCounterStore();

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style scoped>
@media (max-width: 820px) {
  .password_signup {
    flex-direction: column;
  }
  .password_signup {
    flex-direction: column;
    text-align: center;
  }
  .password_signup > .find-password_btn {
    margin: 0 0 1rem;
  }
}
@media (min-width: 821px) {
  .login-container {
    min-width: 500px;
  }
}
.login-main {
  width: 100%;
  height: 100vh;
  background: linear-gradient(to bottom, #00268e, #000c30);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
}
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #02071c;
  border-radius: 2rem;
  margin: 4rem 1rem;
  padding: 3rem 1.5rem;
}
.login-container > h1 {
  margin-top: 0;
  margin-bottom: 2rem;
}

.login-container > form {
  width: 100%;
}
.form__input {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form__input > label {
  margin-bottom: 0.75rem;
}
.form__input > input {
  border-radius: 0.5rem;
  padding: 0.75rem 0.5rem;
}
input[type="submit"] {
  width: 100%;
  color: white;
  font-size: 1.5rem;
  border: none;
  background-color: #0583f2;
  border-radius: 0.3rem;
  margin: 1rem 0;
}

.password_signup {
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin: 1rem 0 1.5rem;
}

.password_signup a {
  text-decoration: none;
  color: #0583f2;
}
.password_signup .signup_label {
  margin-right: 2rem;
}

.divider {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  color: white;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: white;
}

.divider::before {
  margin: 0 0.5rem 0 0;
}

.divider::after {
  margin: 0 0 0 0.5rem;
}
.social-login {
  width: 100%;
  display: flex;
  justify-content: center;
}
.social-login > div {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: white;
  padding: 0.5rem;
}
.social-login > div > img {
  width: 100%;
  height: 100%;
}
.social-login > .social__kakao {
  margin-left: 3rem;
  background-color: yellow;
}
</style>
