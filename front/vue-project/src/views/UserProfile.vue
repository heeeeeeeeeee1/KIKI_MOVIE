<template>
  <div>
    <h1>사용자 프로필</h1>
    <p>Username: {{ profileData.username }}</p>
    <p>Email: {{ profileData.email }}</p>
    <p>Gender: {{ profileData.gender }}</p>
    <p>Birth Date: {{ profileData.birth_date }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const profileData = ref({});

onMounted(() => {
  if (store.token) {
    // counter.js에서 프로필 정보 API 호출
    store.fetchUserInfo().then((data) => {
      profileData.value = data;
    });
  }
});
</script>