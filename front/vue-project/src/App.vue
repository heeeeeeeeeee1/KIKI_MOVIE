<template>
  <Header />
  <main>
    <RouterView />
    <TeachableMachine />
  </main>
  <Footer />
</template>

<script setup>
import { RouterView } from "vue-router";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import TeachableMachine from '@/components/TeachableMachine.vue'
</script>

<style>
@import "@/assets/styles/base/reset.css";
@import "@/assets/styles/base/variable.css";
@import "@/assets/styles/base/main.css";
</style>

<style scoped>
main {
  padding-top: 3rem;
}
</style>
