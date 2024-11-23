<!-- UserEditView -->
<template>
  <main class="user-edit">
    <div class = "profile-image">
      <img src="@/assets/basic-profile.png" alt="profile-pic" />
    </div>
    
    <form class="user-info">
      <div class="form__input">
        <label for="email">Email</label>
        <input id="email" v-model="formData.email" />
      </div>
      <div class="form__input">
        <label for="nickname">닉네임</label>
        <input id="nickname" v-model="formData.nickname" />
      </div>
      <div class="form__input">
        <label for="introduce">소개</label>
        <input id="introduce" v-model="formData.introduce" />
      </div>
      <div class="form__input">
        <label for="password1">비밀번호</label>
        <input id="password1" v-model="formData.password1" type="password"/>
      </div>
      <div class="form__input">
        <label for="password2">비밀번호 확인</label>
        <input id="password2" v-model="formData.password2" type="password"/>
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
        <!-- 회원탈퇴시 알람 -->
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

// 사용자 입력 폼 데이터
const formData = ref({
  nickname: '',
  email: '',
  introduce: '',
  password1: '',
  password2: '',
  gender: '',
  birth_date: '',
})

// 초기 데이터 저장(회원 정보 수정 중 취소 시 복구용)
const initialFormData = ref({});

// 마운트 시 사용자 프로필 정보 가져오기
onMounted(() => {
  store.fetchUserProfile()
    .then((data) => {
      formData.value = {
        email: data.email || '',
        nickname: data.username || '',
        introduce: data.introduce || '',
        password1: '',
        password2: '',
        gender: data.gender || '',
        birth_date: data.birth_date || '',
      };
      initialFormData.value = { ...formData.value };
    })
    .catch((error) => {
      console.error('프로필 정보 로딩 실패:', error);
    });
});


// 회원 탈퇴
const dropAccount = () => {
  if (confirm("정말로 계정을 삭제하시겠습니까?")) {
    store.logOut(); // Store에서 로그아웃 처리
    alert("계정이 삭제되었습니다.")
    router.push("/") // 프로필 페이지로 이동
  }
}

// 사용자 정보 업데이트
const updateProfile = () => {
  store.updateUserInfo(formData.value)
    .then(() => {
      alert('정보가 성공적으로 업데이트되었습니다.');
      router.push('/profile'); // 프로필 페이지로 이동
    })
    .catch((err) => {
      alert('정보 업데이트에 실패했습니다.');
      console.error(err);
    });
};

// 취소 버튼
const cancelEdit = () => {
  formData.value = { ...initialFormData.value } // 초기 상태 복원
};

</script>

<style scoped>
@import "@/assets/styles/components/userEdit.css";
</style>