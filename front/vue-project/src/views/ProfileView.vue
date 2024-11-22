<!-- ProfileView -->
<template>
    <div class="profile-view">
      <!-- 사용자 정보 표시 -->
      <ProfileInfo :user="user" />
  
      <!-- "봤어요", "보고싶어요" 버튼 -->
      <ProfileReaction
        @switchList="switchMovieList"
        :activeList="activeList"
      />
  
      <!-- 영화 리스트 표시 -->
      <section>
        <h3>{{ activeList === 'watched' ? '본 영화 리스트' : '보고 싶은 영화 리스트' }}</h3>
        <div class="movie-list">
          <div
            v-for="movie in displayedMovies"
            :key="movie.id"
            class="movie-card"
          >
            <h4>{{ movie.title }}</h4>
            <p>{{ movie.description }}</p>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import ProfileInfo from "./ProfileInfo.vue";
  import ProfileReaction from "./ProfileReaction.vue";
  import { useMovieStore } from "@/stores/movieStore";
  
  const movieStore = useMovieStore();
  
  // 사용자 데이터 (회원가입 시 입력받은 데이터)
  const user = ref({
    nickname: "사용자 닉네임",
    ageGroup: "20대",
    gender: "여성",
    email: "example@email.com",
    bio: "영화를 좋아하는 영화광입니다!",
  });
  
  // 초기 상태
  const activeList = ref("watched"); // 'watched' 또는 'wishlist'
  const displayedMovies = ref([]);
  
  // 영화 데이터 초기화
  const initMovies = async () => {
    try {
      // 본 영화와 보고 싶은 영화 데이터를 가져오기
      const watchedMovies = await movieStore.getMoviesByType("watched");
      const wishlistMovies = await movieStore.getMoviesByType("wishlist");
  
      // 초기 표시 영화 리스트 설정
      displayedMovies.value =
        activeList.value === "watched" ? watchedMovies : wishlistMovies;
    } catch (err) {
      console.error("영화 데이터를 초기화하는 중 오류:", err);
    }
  };
  
  // 리스트 전환
  const switchMovieList = (listType) => {
    activeList.value = listType;
    displayedMovies.value =
      listType === "watched"
        ? movieStore.getMoviesByType("watched")
        : movieStore.getMoviesByType("wishlist");
  };
  
  // 컴포넌트 초기화
  initMovies();
  </script>