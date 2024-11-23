<template>
  <main class="signup-main">
    <section class="signup-left">
      <div>
        <h1>
          당신의 데이터를 기반으로<br/>
          개인 맞춤형 영화 추천을<br/>
          경험해보세요
        </h1>
      </div>
    </section>
    <section class="signup-right">
      <div class="right__form">
        <h1>Sign Up</h1>
        <form @submit.prevent="signUp">
          <div class="form__input">
            <label for="email">이메일</label>
            <input type="email" id="email" v-model.trim="email" required/>
          </div>
          <div class="form__input">
            <label for="username">닉네임</label>
            <input type="text" id="username" v-model.trim="username" required/>
          </div>
          <div class="form__input">
            <label for="password1">비밀번호</label>
            <input type="password" id="password1" v-model.trim="password1" required/>
          </div>
          <div class="form__input">
            <label for="password2">비밀번호 확인</label>
            <input type="password" id="password2" v-model.trim="password2" required/>
          </div>
          <div class="form__input">
            <label for="gender">성별</label>
            <div class="input_gender">
              <input type="button" id="male" value="남성" :class="{ selected: gender === 'male' }" @click="gender = 'male'"/>
              <input type="button" id="female" value="여성" :class="{ selected: gender === 'female' }" @click="gender = 'female'"/>
            </div>
          </div>
          <div class="form__input">
            <label for="birth_date">태어난 년도</label>
            <input type="date" id="birth_date" v-model="birth_date" required/>
          </div>
          <input type="submit" value="회원가입" />
        </form>
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
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    gender: gender.value,
    email: email.value,
    birth_date: birth_date.value,
  };
  store.signUp(payload);

  router.push({ name: "LogInView" })

};
</script>

<style scoped>
@media (max-width: 820px) {
  .signup-main {
    flex-direction: column;
  }
  .signup-main > section {
    width: 100%;
  }
  .signup-main > .signup-left > div {
    width: 100%;
    border: none;
    margin: 2rem 0 0;
  }
  .signup-left h1 br:last-child {
    display: none;
  }
  .signup-left h1 {
    width: 100%;
    text-align: center;
    font-size: 1.5rem;
  }
  .right__form {
    width: 80%;
    margin: 2rem 0 4rem;
  }
}
@media (min-width: 820px) {
  .signup-main {
    flex-direction: row;
  }
  .signup-main > section {
    width: 50%;
  }
  .signup-left h1 {
  margin: 3rem auto;
  font-size: 2.5rem;
  line-height: 3.5rem;
  text-wrap: nowrap;
  }
  .right__form {
    width: 60%;
    margin: 2rem 0;
  }
}
.signup-main {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(to bottom, #00268e, #000c30);
  display: flex;
  justify-content: ceneter;
  align-items: center;
  color: white;
}
.signup-main > section {
  display: flex;
  justify-content: center;
  align-items: center;
}
.signup-left > div {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5rem auto;
  border-right: 1px solid darkgray;
}
.signup-left h1 {
  text-wrap: nowrap;
}
.right__form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #02071c;
  border-radius: 2rem;
  padding: 3rem 1.5rem;
}
.right__form > h1 {
  margin-top: 0;
  margin-bottom: 2rem;
}

.right__form form {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form__input {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-bottom: 1rem;
}

.form__input > label {
  margin-bottom: 0.5rem;
}
.form__input > input {
  border-radius: 0.5rem;
  padding: 0.5rem;
}

.input_gender {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.input_gender input[type="button"] {
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s;
  width: 49%;
  padding: 0.5rem;
  color: black;
  border-radius: 0.5rem;
}

/* 선택된 버튼 스타일 */
.input_gender input[type="button"].selected {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
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
