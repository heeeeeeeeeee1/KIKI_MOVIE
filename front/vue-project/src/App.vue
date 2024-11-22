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
    <div class="header-container">
      <nav class="left-menu">
        <span class="nav-text logo">로고</span>
        <RouterLink :to="{ name: 'MainHomeView' }" class="nav-text home"
          >홈</RouterLink
        >
      </nav>
      <nav class="right-users">
        <div v-if="!store.isLogin">
          <RouterLink
            :to="{ name: 'SignUpView' }"
            class="nav-text users__signup"
            >회원가입</RouterLink
          >
          <RouterLink :to="{ name: 'LogInView' }" class="nav-text users__login"
            >로그인</RouterLink
          >
        </div>
        <div v-else>
          <a href="">{{ store.username }}</a>
          <form @submit.prevent="logOut">
            <input
              type="submit"
              value="Logout"
              class="nav-text users__logout"
            />
          </form>
        </div>
      </nav>
    </div>
  </header>
  <main>
    <RouterView />
  </main>
  <footer></footer>
</template>

<style scoped>
/* header 관련 설정 */
header {
  width: 100%;
  height: 2rem;
  display: flex;
  justify-content: center;
  background-color: black;
  position: fixed;
  z-index: 1;
}

header .header-container {
  width: 70%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

header nav {
  height: 100%;
  display: flex;
  align-items: center;
  margin: 0;
}

nav .nav-text {
  text-decoration: none;
  color: white;
}

nav .nav-text:not(:last-child) {
  margin-right: 1rem;
}

nav.right-users {
  justify-content: flex-end;
}

nav .logo nav a.router-link-exact-active {
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

main {
  padding-top: 1rem;
}
</style>
