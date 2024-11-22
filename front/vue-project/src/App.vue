<template>
  <Header />
  <main>
    <RouterView />
  </main>
  <footer></footer>
</template>

<script setup>
import { RouterView } from "vue-router";
import Header from "@/components/Header.vue";
</script>

<style>
@import "@/assets/styles/base/reset.css";
@import "@/assets/styles/base/variable.css";
@import "@/assets/styles/base/main.css";
</style>

<style scoped>
main {
  padding-top: 1rem;
}
</style>
