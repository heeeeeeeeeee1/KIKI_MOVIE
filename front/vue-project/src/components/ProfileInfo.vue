<!--ProfileInfo -->
<template>
  <div class="profile-info">
    <div class="profile-image">
      <img src="@/assets/basic-profile.png" alt="profile-pic" />
    </div>
    <div class="profile-text">
      <h3 class="nickname">{{ user.nickname }}</h3>
      <p>{{ user.ageGroup }} {{ user.gender }} | {{ user.email }}</p>
      <p>{{ user.introduce }}</p>
    </div>
    <button class="edit-btn" @click="updateUserInfo">프로필 수정</button>
  </div>
</template>

<script setup>
defineProps(['user']);
const emit = defineEmits(['updateUser']);


const user = {
    nickname: '바키',
    ageGroup: '20대',
    gender: '여성',
    email: 'email@example.com',
    introduce: '태일아 배고파',
}
</script>

<style scoped>
@import "@/assets/styles/components/profileInfo.css";
</style>
