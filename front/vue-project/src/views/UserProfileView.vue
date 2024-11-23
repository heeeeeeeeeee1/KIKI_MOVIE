<-- UserProfileView.vue -->
<template>
  <div class="user-profile">
    <ProfileInfo />

    <ProfileReaction 
      :activeList="activeList" 
      @switchList="updateActiveList"
    />
  </div>
</template>


<script setup>
import { ref } from 'vue';
import ProfileInfo from '@/components/ProfileInfo.vue';
import ProfileReaction from '@/components/ProfileReaction.vue';

const activeList = ref('watched'); // 초기 상태: "봤어요"

// switchList 이벤트를 통해 activeList 업데이트
const updateActiveList = (listName) => {
  console.log('Switching list to:', listName); // 디버깅 로그
  activeList.value = listName; // 상태 업데이트
};

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
