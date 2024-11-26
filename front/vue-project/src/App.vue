<template>
  <Header v-if="!route.meta.hideHeader" />
  <main :class="{ 'no-padding': route.meta.hideHeader }">
    <RouterView />
    <ActorSearch />
  </main>
  <Footer />
</template>

<script setup>
import { useRoute } from "vue-router";
import { RouterView } from "vue-router";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import ActorSearch from "@/Views/ActorSearch.vue";

const route = useRoute();
</script>

<style>
@import "@/assets/styles/base/reset.css";
@import "@/assets/styles/base/variable.css";
@import "@/assets/styles/base/main.css";
</style>

<style scoped>
main {
  padding-top: 3rem;
  position: relative;
  min-height: 700px;
}

main.no-padding {
  padding-top: 0;
}
</style>