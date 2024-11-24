<!-- UserEditView -->
<template>
  <main class="user-edit">
    <div class="profile-image">
      <img src="@/assets/basic-profile.png" alt="profile-pic" />
    </div>
    
    <form class="user-info">
      <div class="form__input">
        <label for="email">Email</label>
        <input id="email" v-model="formData.email" />
      </div>
      <div class="form__input">
        <label for="nickname">닉네임</label>
        <!-- 읽기 전용으로 username 변경 불가 -->
        <input id="nickname" v-model="formData.nickname" disabled />
        <small style="color: gray;">닉네임은 변경할 수 없습니다.</small>
      </div>
      <div class="form__input">
        <label for="introduce">소개</label>
        <input id="introduce" v-model="formData.introduce" />
      </div>
      <div class="form__input">
        <label for="gender">성별</label>
        <select id="gender" v-model="formData.gender">
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>
      <div class="form__input">
        <label for="birth_date">생년월일</label>
        <input id="birth_date" v-model="formData.birth_date" type="date" />
      </div>
    </form>

    <div class="btn-group">
      <div class="left-btn">
        <!-- 회원탈퇴 버튼 : 현재 해당 기능 동작 안함, 수정 필요-->
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
import { ref, onMounted } from 'vue';
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

const initialFormData = ref({});

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

onMounted(() => {
  store.fetchUserProfile()
    .then((data) => {
      formData.value = {
        email: data.email || '',
        nickname: data.username || '',
        introduce: data.introduce || '',
        gender: genderMap[data.gender] || '',
        birth_date: data.birth_date || '',
      };
      initialFormData.value = { ...formData.value };
    })
    .catch((error) => {
      console.error('프로필 정보 로딩 실패:', error);
    });
});

const reverseGenderMap = {
  male: 'M',
  female: 'W',
};

const updateProfile = () => {
  const updatedData = getChangedFields(initialFormData.value, formData.value);

  if (Object.keys(updatedData).length === 0) {
    alert('변경된 내용이 없습니다.');
    return;
  }

  store.updateUserInfo(updatedData)
    .then((res) => {
      alert('정보가 성공적으로 업데이트되었습니다.');
      router.push('/profile');
    })
    .catch((err) => {
      console.error('사용자 정보 업데이트 실패:', err.response?.data || err);
      alert(`업데이트 실패: ${JSON.stringify(err.response?.data)}`);
    });
};

const cancelEdit = () => {
  formData.value = { ...initialFormData.value };
};

const dropAccount = () => {
  if (confirm('정말로 계정을 삭제하시겠습니까?')) {
    store.logOut();
    alert('계정이 삭제되었습니다.');
    router.push('/');
  }
};
</script>

<style scoped>
@import "@/assets/styles/components/userEdit.css";
</style>