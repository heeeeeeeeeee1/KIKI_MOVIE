<template>
  <main class="main-home-container">
    <div class="main-home">
      <button @click="openActorModal">배우 선택하고 영화 추천 받기</button>
      <BoxOfficeSlide />
      <PopularReviewList />
      <MyGenrePopular />
      <MyAgePopular />


      <!-- 배우 선택 모달 -->
      <SelectActorModal
        v-if="isActorModalVisible"
        :is-visible="isActorModalVisible"
        :actors="actors"
        @close="closeActorModal"
        @confirm="handleActorSelection"
      />

      <!-- 추천 영화 모달 -->
      <MovieRecommendationModal
        v-if="isMovieModalVisible"
        :is-visible="isMovieModalVisible"
        :movies="movies"
        @close="closeMovieModal"
      />
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import BoxOfficeSlide from "@/components/boxOfficeSlide.vue";
import PopularReviewList from "@/components/popularReviewList.vue";
import MyGenrePopular from "@/components/myGenrePopular.vue";
import MyAgePopular from "@/components/myAgePopular.vue";
import SelectActorModal from "@/components/SelectActorModal.vue";
import MovieRecommendationModal from "@/components/MovieRecommendationModal.vue";
import { getPopularActors, getMoviesByActor } from "@/api/tmdb";

// 상태 관리
const isActorModalVisible = ref(false); // 배우 선택 모달 표시 여부
const isMovieModalVisible = ref(false); // 추천 영화 모달 표시 여부
const actors = ref([]); // 배우 리스트
const movies = ref([]); // 추천 영화 리스트

// 배우 선택 모달 열기
const openActorModal = async () => {
  try {
    const response = await getPopularActors();
    actors.value = response.sort(() => Math.random() - 0.5).slice(0, 10); // 랜덤 배우 10명
    isActorModalVisible.value = true; // 모달 표시
  } catch (error) {
    console.error("배우 데이터를 불러오는 중 오류 발생:", error);
  }
};

// 배우 선택 모달 닫기
const closeActorModal = () => {
  isActorModalVisible.value = false;
};

// 추천 영화 모달 닫기
const closeMovieModal = () => {
  isMovieModalVisible.value = false;
};

// 배우 선택 처리
const handleActorSelection = async (selectedActors) => {
  try {
    isActorModalVisible.value = false; // 배우 선택 모달 닫기
    isMovieModalVisible.value = true; // 추천 영화 모달 열기

    const movieCounts = {}; // 영화 중복 횟수 저장

    // 선택된 배우 데이터를 순회
    for (const actor of selectedActors) {
      const actorMovies = await getMoviesByActor(actor.id);

      // 유효성 검사: 영화 데이터가 비어있거나 없는 경우 처리
      if (!actorMovies || actorMovies.length === 0) {
        console.warn(`배우 ${actor.name}의 영화 데이터를 찾을 수 없습니다.`);
        continue;
      }

      actorMovies.forEach((movie) => {
        movieCounts[movie.id] = (movieCounts[movie.id] || 0) + 1;
      });
    }

    // 중복 횟수로 정렬 후 상위 3개 영화 선택
    movies.value = Object.entries(movieCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([id]) => {
        return selectedActors.flatMap((actor) => actor.movies || []).find((m) => m.id === Number(id));
      })
      .filter(Boolean); // 유효하지 않은 데이터 제거
  } catch (error) {
    console.error("추천 영화 생성 중 오류 발생:", error);
  }
};

</script>

<style scoped>
.main-home-container {
  display: flex;
  justify-content: center;
}

.main-home {
  width: 70%;
  overflow: hidden;
}

button {
  padding: 10px 20px;
  margin-top: 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
