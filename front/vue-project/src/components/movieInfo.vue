<template>
  <section class="movie-info" v-if="movie">
    <div>
      <div class="info-left">
        <img :src="tmdb_base_url + movie.poster_path" alt="영화 포스터" />
      </div>
    </div>
    <div class="info-right">
      <div class="info-real">
        <h2>{{ movie.title }}</h2>
        <h3>{{ movie.original_title }}</h3>
        <hr>
        <p v-if="movie.directors && movie.directors.length > 0">
          감독: {{ movie.directors.slice(0, 5).map(director => director.name).join(", ") }}
          <span v-if="movie.directors.length > 5">
            외 {{ movie.directors.length - 5 }}명
          </span>
        </p>
        <p v-if="movie.actors && movie.actors.length > 0">
          배우: {{ movie.actors.slice(0, 5).map(actor => actor.name).join(", ") }}
          <span v-if="movie.actors.length > 5">
            외 {{ movie.actors.length - 5 }}명
          </span>
        </p>
        <p v-else>배우 정보가 없습니다.</p>
        <p v-if="movie.genres && movie.genres.length > 0">
          장르: {{ movie.genres.map(genre => genre.name).join(", ") }}
        </p>
        <p v-else>장르 정보가 없습니다.</p>
        <p v-if="movie.description">
          {{ isExpanded ? movie.description : truncatedDescription }}
          <button @click="toggleDescription" class="more-flip-btn">
            {{ isExpanded ? "접기" : "더보기" }}
          </button>
        </p>
        <p v-else>시놉시스가 없습니다.</p>
      </div>
      <!-- <MovieReaction /> -->
    </div>
  </section>
  <p v-else>
    영화 정보가 없습니다.
  </p>
</template>

<script setup>
import MovieReaction from "@/components/movieReaction.vue";
import { computed, ref } from "vue";

// `props`를 통해 부모 컴포넌트에서 데이터를 받습니다.
const props = defineProps({
  movie: {
    type: Object,
    default: () => ({
      image: "",
      title: "영화 제목 없음",
      original_title: "원제 없음",
      director: "감독 정보 없음",
      actors: [],
      genres: [],
      description: "설명 없음",
    }),
  },
});

// 더보기 상태 관리
const isExpanded = ref(false);
const maxLength = 90; // 줄임 표시를 위한 최대 길이

// 축약된 설명 생성 (m)
const truncatedDescription = computed(() => {
  return props.movie.description.length > maxLength
    ? props.movie.description.slice(0, maxLength) + "..."
    : props.movie.description;
});

// 더보기/접기 상태 토글 함수
const toggleDescription = () => {
  isExpanded.value = !isExpanded.value;
};

const tmdb_base_url = "https://image.tmdb.org/t/p/w500"
</script>

<style scoped>
@import "@/assets/styles/components/movieInfo.css";
</style>
