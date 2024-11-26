<template>
  <header>
    <div class="header-container">
      <nav class="left-menu">
        <RouterLink
          :to="{ name: 'MainHomeView' }"
          class="nav-text logo logo-accounts"
        >
          <div class="img-container">
            <img src="@/assets/kiki_logo.png" alt="키키무비 로고 이미지" />
          </div>
          <span>KIKI</span>
        </RouterLink>
      </nav>
      <nav class="right-users">
        <div v-if="!store.isLogin">
          <RouterLink
            :to="{ name: 'SignUpView' }"
            class="nav-text users__signup"
          >
            회원가입
          </RouterLink>
          <RouterLink :to="{ name: 'LogInView' }" class="nav-text users__login">
            로그인
          </RouterLink>
        </div>
        <div v-else>
          <RouterLink
            :to="{ name: 'UserProfileView' }"
            class="nav-text users__login"
          >
            {{ store.username }}
          </RouterLink>
          <form @submit.prevent="logOut">
            <input
              type="submit"
              value="로그아웃"
              class="nav-text users__logout"
            />
          </form>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const error = ref(false);

const logOut = function () {
  store.logOut();
};

onMounted(() => {
  if (store.token) {
    store
      .fetchUserInfo()
      .then(() => {
        error.value = false;
      })
      .catch((err) => {
        console.log("유저 정보 로드 실패:", err);
        error.value = true;
      });
  } else {
    console.log("유저 정보가 없습니다");
  }
});
</script>

<style scoped>
@import "@/assets/styles/components/header.css";
</style>
