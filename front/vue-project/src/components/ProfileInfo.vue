<!--ProfileInfo -->
<template>
  <div v-if="profileData && profileData.username" class="profile-info">
    <div class="profile-image">
      <img src="@/assets/basic-profile.png" alt="profile-pic" />
    </div>
    <div class="profile-text">
      <h3 class="nickname">{{ profileData.username }}</h3>
      <p>{{ profileData.ageGroup || '연령대' }} {{ profileData.gender || '성별'}} | {{ profileData.email || '정보없음'}}</p>
      <p>{{ profileData.introduce || '소개' }}</p>
    </div>
    <button class="edit-btn" @click="updateUserInfo">프로필 수정</button>
  </div>
    <div v-else>
      <p>사용자 정보를 불러오는 중입니다...</p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted, computed, watch } from 'vue';
import { useCounterStore } from '@/stores/counter';

const router = useRouter()
const store = useCounterStore()

// Pinia의 profileData를 연동
const profileData = computed(() => store.profileData)


// 프로필 수정 페이지로 이동 함수
const updateUserInfo = () => {
  router.push(`/profile/edit/`)
}

// 사용자 프로필 정보 가져오기
const fetchProfile = () => {
  store.fetchUserProfile(); // 사용자 정보 호출
}

onMounted(fetchProfile);

// 라우터 이벤트 감지
watch(() => router.currentRoute.value.path, (newPath) => {
  if (newPath === '/profile') {
    fetchProfile();
  }
});
</script>

<style scoped>
@import "@/assets/styles/components/profileInfo.css";
</style>
