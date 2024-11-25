<!-- UserProfileView.vue -->
<template>
  <!-- 조건 추가: 데이터가 로드되었을 때만 렌더링 -->
  <ProfileInfo :profileData="userData" />
  <div class="user-profile">
    <ProfileReaction 
      :activeList="activeList" 
      :watchedMovies="watchedMovies" 
      :wishlistMovies="wishlistMovies"
      @switchList="updateActiveList"
    />
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { storeToRefs } from 'pinia';
import ProfileInfo from '@/components/ProfileInfo.vue';
import ProfileReaction from '@/components/ProfileReaction.vue';

const store = useCounterStore(); // Pinia 스토어 사용
const isLoading = ref(true);
const activeList = ref('watched'); // 초기 상태: "봤어요"

const { profileData: userData, watchedReviews: watchedMovies, wishlistMovies } = storeToRefs(store);
// 데이터 가져오기
const fetchUserData = async () => {
  try {
    await store.fetchUserProfile();
    // .value를 사용하여 반응형 참조의 실제 값에 접근
    console.log('vue 프로필 데이터:', userData.value);
    console.log('vue 봤어요:', watchedMovies.value);
    console.log('vue 보고싶어요:', wishlistMovies.value);
    isLoading.value = false;
  } catch (error) {
    console.error('사용자 데이터 가져오기 실패:', error);
    isLoading.value = false;
  }
};


// 리스트 전환
const updateActiveList = (listName) => {
  activeList.value = listName;
};

// switchList 이벤트를 통해 activeList 업데이트
// const updateActiveList = (listName) => {
//   console.log('Switching list to:', listName); // 디버깅 로그
//   activeList.value = listName; // 상태 업데이트
// };

// API 데이터 가져오기
onMounted(fetchUserData);

</script>

<style scoped>
.user-profile {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center; 
  padding: 1rem; 
}

</style>
