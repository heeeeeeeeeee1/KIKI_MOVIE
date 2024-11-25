<template>
  <div class="actor-search">
    <h2 class="text-xl mb-4">TMDB 배우 ID 매핑 확인</h2>

    <!-- 배우 이름 입력 -->
    <div class="mb-4">
      <label for="actor-name" class="block mb-2 font-bold">배우 이름</label>
      <input
        id="actor-name"
        v-model="actorName"
        type="text"
        placeholder="배우 이름 입력"
        class="w-full p-2 border rounded"
      />
    </div>

    <!-- TMDB ID 확인 버튼 -->
    <button
      @click="checkActorId"
      class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      ID 확인
    </button>

    <!-- TMDB에서 검색 버튼 -->
    <button
      @click="searchActorInTMDB"
      class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 ml-2"
    >
      TMDB에서 검색
    </button>

    <!-- 결과 출력 -->
    <div v-if="actorId" class="mt-4 p-4 bg-gray-50 rounded">
      <p><strong>배우 이름:</strong> {{ actorName }}</p>
      <p><strong>TMDB ID:</strong> {{ actorId }}</p>
    </div>

    <div v-if="tmdbSearchResults.length > 0" class="mt-8">
      <h3 class="font-bold mb-2">TMDB 검색 결과</h3>
      <ul>
        <li
          v-for="(result, index) in tmdbSearchResults"
          :key="index"
          class="mb-2"
        >
          {{ result.name }} (ID: {{ result.id }})
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { getActorId } from "../api/actorMapping";
import axios from "axios";

// TMDB API 설정
const API_KEY = "700c493de1fec79592154b7cb6361039";
const BASE_URL = "https://api.themoviedb.org/3";

// 데이터 및 함수 선언
const actorName = ref("");
const actorId = ref(null);
const tmdbSearchResults = ref([]);

// 매핑 데이터에서 ID 확인
const checkActorId = () => {
  actorId.value = getActorId(actorName.value);
  if (!actorId.value) {
    alert("매핑 데이터에 해당 배우가 없습니다.");
  }
};

// TMDB에서 배우 검색
const searchActorInTMDB = async () => {
  if (!actorName.value.trim()) {
    alert("배우 이름을 입력하세요.");
    return;
  }

  try {
    const response = await axios.get(`${BASE_URL}/search/person`, {
      params: {
        api_key: API_KEY,
        query: actorName.value,
        language: "ko-KR", // 한글로 응답
      },
    });

    if (response.data.results.length > 0) {
      tmdbSearchResults.value = response.data.results;
    } else {
      alert("TMDB에서 해당 배우를 찾을 수 없습니다.");
    }
  } catch (error) {
    console.error("TMDB API 호출 오류:", error);
    alert("TMDB API 호출 중 오류가 발생했습니다.");
  }
};
</script>

<style>
.actor-search {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}
div {
    color: white;
}
button {
    background-color: blue;
}
</style>
