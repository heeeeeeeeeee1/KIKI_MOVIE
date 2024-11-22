<template>
  <header>
    <div class="header-container">
      <nav class="left-menu">
        <span class="nav-text logo">로고</span>
        <RouterLink :to="{ name: 'MainHomeView' }" class="nav-text home">
          홈
        </RouterLink>
      </nav>
      <nav class="right-users">
        <div v-if="!store.isLogin">
          <RouterLink :to="{ name: 'SignUpView' }" class="nav-text users__signup">
            회원가입
          </RouterLink>
          <RouterLink :to="{ name: 'LogInView' }" class="nav-text users__login">
            로그인
          </RouterLink>
        </div>
        <div v-else>
          <a href="" class="nav-text">{{ store.username }}</a>
          <form @submit.prevent="logOut">
            <input type="submit" value="로그아웃" class="nav-text users__logout"/>
          </form>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const error = ref(false);

const logOut = function () {
  store.logOut();
};

onMounted(() => {
  if (store.token) {
    store.fetchUserInfo()
      .then(() => {
        error.value = false;
      })
      .catch((err) => {
        console.log('유저 정보 로드 실패:', err);
        error.value = true;
      });
  } else {
    console.log("유저 정보가 없습니다");
  }
});
</script>

<style scoped>
header {
  width: 100%;
  height: 2.5rem;
  display: flex;
  justify-content: center;
  position: fixed;
  z-index: 1;
}

.header-container {
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

.nav-text {
  text-decoration: none;
  color: white;
}

.nav-text:not(:last-child) {
  margin-right: 1rem;
}

.right-users {
  justify-content: flex-end;
}

.right-users div{
  display: flex;
  align-items: center;
  justify-content: center;
  justify-content: flex-end;
}

.logo nav a.router-link-exact-active {
  color: white;
}

.right-users form {
  height: 100%;
}

.users__logout {
  background-color: transparent;
  border: none;
  height: 100%;
  padding: 0;
  line-height: 1.5rem;
}
</style>
