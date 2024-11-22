<template>
  <form @submit.prevent="updateProfile">
    <label for="username">Username</label>
    <input id="username" v-model="formData.username" />

    <label for="email">Email</label>
    <input id="email" v-model="formData.email" />

    <label for="gender">Gender</label>
    <select id="gender" v-model="formData.gender">
      <option value="male">Male</option>
      <option value="female">Female</option>
    </select>

    <label for="birth_date">Birth Date</label>
    <input id="birth_date" v-model="formData.birth_date" type="date" />

    <button type="submit">Update</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const formData = ref({
  username: '',
  email: '',
  gender: '',
  birth_date: '',
});

// 사용자 정보 업데이트 함수
const updateProfile = () => {
  store.updateUserInfo(formData.value).then(() => {
    alert('정보가 성공적으로 업데이트되었습니다.');
  });
};
</script>
