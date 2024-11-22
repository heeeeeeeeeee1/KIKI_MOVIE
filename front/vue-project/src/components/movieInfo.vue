<template>
  <section class="movie-info" v-if="movie">
    <div>
      <div class="info-left">
        <img :src="movie.image" alt="영화 포스터" />
      </div>
    </div>
    <div class="info-right">
      <div class="info-real">
        <h2>{{ movie.title }}</h2>
        <h3>{{ movie.original_title }}</h3>
        <p>감독: {{ movie.director }}</p>
        <p>배우: {{ movie.actors.join(", ") }}</p>
        <p>장르: {{ movie.genres.join(", ") }}</p>
        <p>{{ movie.description }}</p>
      </div>
      <MovieReaction />
    </div>
  </section>
  <p v-else></p>
</template>

<script setup>
import MovieReaction from "@/components/movieReaction.vue";
import { ref } from "vue";

const movie = ref({
  image:
    "https://t1.daumcdn.net/thumb/R720x0.fjpg/?fname=http://t1.daumcdn.net/brunch/service/user/b5EX/image/cUMlhhRXhvyfpDG0ENjt9NM5stU.jpg",
  title: "미드소마",
  originalTitle: "Midsommar",
  director: "아리 애스터",
  actors: [
    "플로렌스 퓨",
    "잭 레이너",
    "윌 폴터",
    "빌헬름 브롬그렌",
    "윌리엄 잭슨 하퍼",
  ],
  genres: [
    "공포",
    "미스터리",
    "드라마",
    "스릴러",
    "어드벤처",
    "서스펜스",
    "블랙 코미디",
    "오컬트",
    "고어",
  ],
  description:
    "2019년에 개봉한 아리 애스터 감독의 공포 영화.불행한 사건으로 인해 큰 슬픔에 빠진 주인공 대니가 스웨덴인 친구 펠레의 초대를 받아 90년에 한번씩 9일간 하지 축제가 열리는 '호르가(Hårga)'라는 스웨덴의 작은 마을에 방문해서 겪는 일들을 다루는 내용이다.",
});
</script>

<style scoped>
@import "@/assets/styles/components/movieInfo.css";
</style>
