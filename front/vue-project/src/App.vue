<style>
@import "@/assets/styles/base/reset.css";
@import "@/assets/styles/base/variable.css";
@import "@/assets/styles/base/main.css";
</style>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();

const logOut = function () {
  store.logOut();
};
</script>

<template>
  <header>
    <nav class="left-menu">
      <span>로고</span>
      <a href="">홈</a>
      <a href="">영화</a>
      <!-- <RouterLink :to="{ name: 'home' }">홈</RouterLink>
      <RouterLink :to="{ name: 'movie' }">영화</RouterLink> -->
    </nav>
    <nav class="right-users">
      <div v-if="!store.isLogin">
        <RouterLink :to="{ name: 'SignUpView' }" class="users__signup"
          >회원가입</RouterLink
        >
        <RouterLink :to="{ name: 'LogInView' }" class="users__login"
          >로그인</RouterLink
        >
      </div>
      <div v-else>
        <a href="">{{ store.username }}</a>
        <form @submit.prevent="logOut">
          <input type="submit" value="Logout" class="users__logout" />
        </form>
      </div>
    </nav>
  </header>
  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  text-wrap: nowrap;
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}

/* 새롭게 작성한 내용 */
header {
  width: 100%;
  min-height: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: black;
  padding: 0.5rem 0;
  /* position: fixed; */
}

nav {
  height: 100%;
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0 1rem;
}
nav.right-users {
  justify-content: flex-end;
}
nav > a,
span,
.logo,
.users__logout,
.users__signup,
.users__login {
  text-decoration: none;
  color: white;
}
nav a.router-link-exact-active {
  color: white;
}
.right-users form {
  height: 100%;
}
.users__logout {
  background-color: transparent;
  border: none;
  height: 100%;
  padding: 0 1rem;
  line-height: 1.5rem;
}
</style>
