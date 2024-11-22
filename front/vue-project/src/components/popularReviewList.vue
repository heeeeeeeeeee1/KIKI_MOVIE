<template>
  <section>
    <h3>인기 영화 추천</h3>
    <div class="container">
      <ul
        class="boxes"
        @mouseover="pauseAnimation"
        @mouseleave="resumeAnimation"
      >
        <!-- 원본 리스트 -->
        <li
          v-for="movie in popularMovies"
          :key="movie.id"
          class="movie-item"
        >
          <router-link :to="`/movies/${movie.id}`" class="movie-link">
            <div class="movie-img-container">
              <img :src="movie.poster" :alt="movie.title" />
            </div>
            <p class="movie-title">{{ movie.title }}</p>
          </router-link>
        </li>
        <!-- 복제 리스트 -->
        <li
          v-for="movie in popularMovies"
          :key="`copy-${movie.id}`"
          class="movie-item"
        >
          <router-link :to="`/movies/${movie.id}`" class="movie-link">
            <div class="movie-img-container">
              <img :src="movie.poster" :alt="movie.title" />
            </div>
            <p class="movie-title">{{ movie.title }}</p>
          </router-link>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const popularMovies = ref([
  {
    id: 1,
    title: 'Movie 1',
    poster:
      'https://upload.wikimedia.org/wikipedia/ko/0/02/%EC%9D%B8%EC%82%AC%EC%9D%B4%EB%93%9C_%EC%95%84%EC%9B%83_2_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg',
  },
  {
    id: 2,
    title: 'Movie 2',
    poster:
      'https://cdn-dantats.stunning.kr/prod/portfolios/dfab4ac1-c0db-406b-962c-59c3b9fd45c5/contents/HwiHNxqZ8EJNtgPX.%EB%AA%A8%EC%85%98%EB%94%94%EC%9E%90%EC%9D%B8%20%EA%B3%BC%EC%A0%9C7%20%EC%B5%9C%EC%A2%85%EC%88%98%EC%A0%95.jpg.small?q=80&f=webp&t=crop&s=1754x2480',
  },
  {
    id: 3,
    title: 'Movie 3',
    poster:
      'https://mblogthumb-phinf.pstatic.net/MjAxODAxMThfMjE5/MDAxNTE2MjU2NDE5MDU5.hX87C0A0-vcVa5-ME4cVapSnPYVmyAzCXmmyt_NqU7kg.Yy9RLihdKLVIL7Jl7h5p1UpFRBtJBbx3-IKVpxN6UjEg.JPEG.mrnobody0987/%EB%9D%BC%EB%9D%BC%EB%9E%9C%EB%93%9C.jpg?type=w800',
  },
  {
    id: 4,
    title: 'Movie 4',
    poster:
      'https://design.co.kr/wp-content/uploads/2024/03/07_%ED%8C%8C%EB%AC%98_%EC%8A%A4%ED%8E%98%EC%85%9C-%ED%8F%AC%EC%8A%A4%ED%84%B0_%EC%A0%84%EB%8B%AC%EC%9A%A9-832x1189.jpg',
  },
  {
    id: 5,
    title: 'Movie 5',
    poster:
      'https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/201602/19/htm_20160219171437117902.jpg',
  },
]);

const pauseAnimation = (event) => {
  event.currentTarget.style.animationPlayState = 'paused';
};

const resumeAnimation = (event) => {
  event.currentTarget.style.animationPlayState = 'running';
};
</script>

<style scoped>
  @import "@/assets/styles/components/mainMovieScroll.css";
</style>
