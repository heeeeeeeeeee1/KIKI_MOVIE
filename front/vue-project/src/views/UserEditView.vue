<template>
  <main class="user-edit">
    <div class="profile-image">
      <img src="@/assets/basic-profile.png" alt="profile-pic" />
    </div>
    
    <form class="user-info">
      <div class="form__input">
        <label for="email">Email</label>
        <input 
          id="email" 
          v-model="formData.email"
          disabled
        />
        <small style="color: gray;">이메일은 변경할 수 없습니다.</small>
      </div>
      <div class="form__input">
        <label for="nickname">닉네임</label>
        <input 
          id="nickname" 
          v-model="formData.nickname"
          disabled 
        />
        <small style="color: gray;">닉네임은 변경할 수 없습니다.</small>
      </div>
      <div class="form__input">
        <label for="introduce">소개</label>
        <input 
          id="introduce" 
          v-model="formData.introduce"
          :placeholder="formData.introduce || '자기소개를 입력해주세요'" 
        />
      </div>
      <div class="form__input">
        <label for="gender">성별</label>
        <select 
          id="gender" 
          v-model="formData.gender"
        >
          <option value="">성별을 선택하세요</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>
      <div class="form__input">
        <label for="birth_date">생년월일</label>
        <input 
          id="birth_date" 
          v-model="formData.birth_date" 
          type="date"
        />
      </div>
    </form>

    <div class="btn-group">
      <div class="left-btn">
        <button class="drop-btn" @click.prevent="dropAccount">회원탈퇴</button>
      </div>
      <div class="right-btn">
        <button class="update-btn" @click="updateProfile">수정</button>
        <button class="cancel-btn" @click="cancelEdit">취소</button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const router = useRouter();
const store = useCounterStore();

const formData = ref({
  nickname: '',
  email: '',
  introduce: '',
  gender: '',
  birth_date: '',
});

// formData 변화 감지를 위한 watcher 추가
watch(formData, (newValue) => {
  console.log('formData changed:', newValue);
}, { deep: true });

const initialFormData = ref({});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toISOString().split('T')[0];
};

const getChangedFields = (original, updated) => {
  const changedFields = {};
  for (const key in updated) {
    if (updated[key] !== original[key]) {
      changedFields[key] = updated[key];
    }
  }
  return changedFields;
};

const genderMap = {
  M: 'male',
  W: 'female',
};

onMounted(async () => {
  console.log('Component mounted');
  try {
    console.log('Fetching user profile...');
    const response = await store.fetchUserProfile();
    const profileData = response.profileData;  // profileData 객체 접근
    console.log('Profile data:', profileData);
    
    // 각 필드의 값을 개별적으로 로깅
    console.log('Email:', profileData.email);
    console.log('Username:', profileData.username);
    console.log('Introduce:', profileData.introduce);
    console.log('Gender:', profileData.gender);
    console.log('Birth date:', profileData.birth_date);
    
    const formattedDate = formatDate(profileData.birth_date);
    console.log('Formatted birth date:', formattedDate);
    
    formData.value = {
      email: profileData.email || '',
      nickname: profileData.username || '',
      introduce: profileData.introduce || '',
      gender: genderMap[profileData.gender] || '',
      birth_date: formattedDate,
    };
    
    console.log('FormData after assignment:', formData.value);
    
    initialFormData.value = { ...formData.value };
    console.log('InitialFormData:', initialFormData.value);
  } catch (error) {
    console.error('프로필 정보 로딩 실패:', error);
    console.error('Error details:', {
      message: error.message,
      response: error.response,
      stack: error.stack
    });
    alert('프로필 정보를 불러오는데 실패했습니다.');
  }
});

const reverseGenderMap = {
  male: 'M',
  female: 'W',
};

const updateProfile = async () => {
  console.log('Attempting to update profile');
  console.log('Current formData:', formData.value);
  console.log('Initial formData:', initialFormData.value);
  
  const updatedData = getChangedFields(initialFormData.value, formData.value);
  console.log('Changed fields:', updatedData);

  if (Object.keys(updatedData).length === 0) {
    alert('변경된 내용이 없습니다.');
    return;
  }

  if (updatedData.gender) {
    updatedData.gender = reverseGenderMap[updatedData.gender];
    console.log('Converted gender:', updatedData.gender);
  }

  try {
    console.log('Sending update request with data:', updatedData);
    await store.updateUserInfo(updatedData);
    alert('정보가 성공적으로 업데이트되었습니다.');
    router.push('/profile');
  } catch (error) {
    console.error('Update failed:', error);
    console.error('Error details:', {
      message: error.message,
      response: error.response,
      stack: error.stack
    });
    alert('프로필 업데이트에 실패했습니다.');
  }
};

const cancelEdit = () => {
  console.log('Cancelling edit - Reverting to initial data');
  console.log('Initial data:', initialFormData.value);
  formData.value = { ...initialFormData.value };
};

const dropAccount = async () => {
  if (confirm('정말로 회원 탈퇴를 진행하시겠습니까?\n탈퇴 시 모든 데이터가 삭제되며 이 작업은 되돌릴 수 없습니다.')) {
    try {
      await store.deleteAccount();
      alert('회원 탈퇴가 완료되었습니다.');
      router.push({ name: 'MainHomeView' });  // 이름으로 라우팅
    } catch (error) {
      console.error('회원 탈퇴 실패:', error);
      alert('회원 탈퇴 처리 중 오류가 발생했습니다.');
    }
  }
};
</script>

<style scoped>
@import "@/assets/styles/components/userEdit.css";
</style>