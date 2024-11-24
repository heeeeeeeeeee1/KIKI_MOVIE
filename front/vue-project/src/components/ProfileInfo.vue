<!--ProfileInfo -->
<template>
  <div v-if="profileData && profileData.username" class="profile-info">
    <div class="profile-image">
      <img src="@/assets/basic-profile.png" alt="profile-pic" />
    </div>
    <div class="profile-text">
      <h3 class="nickname">{{ profileData.username }}</h3>
      <p>
        {{ profileData.ageGroup || '연령대' }}
        {{ profileData.gender || '성별'}} |
        {{ profileData.email || '이메일 정보없음'}}
      </p>
      <p>{{ profileData.introduce || '자기 소개가 없습니다.' }}</p>
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
const rawProfileData = computed(() => store.profileData)

const profileData = computed(() => {
  if (!rawProfileData.value) return null;

  const { birth_date, gender, introduce, ...rest } = rawProfileData.value;

  // 성별 변환
  const genderMap = {
    M: '남성',
    W: '여성',
  };

  // 연령대 계산
  let ageGroup = null;
  if (birth_date) {
    const birthYear = new Date(birth_date).getFullYear();
    const currentYear = new Date().getFullYear();
    const age = currentYear - birthYear;

    if (age === 0) {
      const birthMonth = new Date(birth_date).getMonth();
      const currentMonth = new Date().getMonth();
      if (currentMonth === birthMonth) {
        ageGroup = '응애 애기'; // 올해 태어난 경우
      } else {
        ageGroup = '잼민이'; // 0살로 계산된 경우
      }
    } else {
      ageGroup = `${Math.floor(age / 10) * 10}대`;
    }
  }

  return {
    ...rest,
    gender: genderMap[gender] || '성별',
    ageGroup: ageGroup || '연령대',
    introduce: introduce || '자기소개가 없습니다',
  };
});

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
