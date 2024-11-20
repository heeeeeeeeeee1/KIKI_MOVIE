<template>
  <main class="signup-main">
    <div class="signup-promo">
      <h1>
        당신의 데이터를 기반으로<br />개인 맞춤형 영화 추천을<br />경험해보세요
      </h1>
    </div>
    <div class="signup-form">
      <h1>Sign Up</h1>
      <form @submit.prevent="signUp">
        <div class="signup-form__input">
          <label for="username">username</label>
          <input type="text" id="username" v-model.trim="username" />
        </div>
        <div class="signup-form__input">
          <label for="password1">password</label>
          <input type="password" id="password1" v-model.trim="password1" />
        </div>
        <div class="signup-form__input">
          <label for="password2">password confirmation</label>
          <input type="password" id="password2" v-model.trim="password2" />
        </div>
        <div class="signup-form__input">
          <label for="gender">gender</label>
          <div class="input_gender">
            <input type="button" id="male" value="male" v-model="gender" />
            <input type="button" id="female" value="female" v-model="gender" />
          </div>
        </div>
        <div class="signup-form__input">
          <label for="email">email</label>
          <input type="email" id="email" v-model.trim="email" />
        </div>
        <div class="signup-form__input">
          <label for="birth_date">birth date</label>
          <input type="date" id="birth_date" v-model="birth_date" />
        </div>
        <input type="submit" value="회원가입" />
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const gender = ref(null); // 성별
const email = ref(null); // 이메일
const birth_date = ref(null); // 생년월일

const store = useCounterStore();

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
};
</script>

<style scoped>
.signup-main {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(to bottom, #00268e, #000c30);
  display: flex;
  color: white;
}
.signup-promo {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.signup-promo > h1 {
  display: block;
  width: 50%;
  padding: 5rem 1.5rem;
  border-right: 1px solid lightgray;
}
.signup-form {
  display: flex;
  width: 500px;
  margin: 3rem;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #02071c;
  border-radius: 2rem;
  padding: 1.5rem;
}

.signup-form > form {
  width: 100%;
}

.signup-form__input {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 1rem;
}

.signup-form__input > label {
  margin-bottom: 0.5rem;
}
.signup-form__input > input {
  width: 100%;
  height: 1.5rem;
  border-radius: 0.3rem;
}

.input_gender {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.input_gender > input[type="button"] {
  width: 49%;
  height: 1.5rem;
  color: black;
}

input[type="submit"] {
  width: 100%;
  height: 2rem;
  color: white;
  border: none;
  background-color: #0583f2;
  border-radius: 0.3rem;
}
</style>
