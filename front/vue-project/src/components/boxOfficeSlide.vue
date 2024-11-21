<template>
  <div class="coverflow-wrapper">
    <!-- 왼쪽 화살표 -->
    <button class="arrow left-arrow" @click="prevSlide">‹</button>

    <!-- 커버플로우 -->
    <div
      class="coverflow-container"
      @mousedown="startDrag"
      @mousemove="onDrag"
      @mouseup="stopDrag"
      @mouseleave="stopDrag"
    >
      <div
        class="coverflow-item"
        v-for="(movie, index) in movies"
        :key="movie.id"
        :class="{ active: index === currentIndex }"
        :style="getStyle(index)"
        @mouseover="hoverToCenter(index)"
        @click="goToDetail(movie.id)"
      >
        <img :src="movie.poster" alt="Movie Poster" />
        <p class="title">{{ movie.title }}</p>
      </div>
    </div>

    <!-- 오른쪽 화살표 -->
    <button class="arrow right-arrow" @click="nextSlide">›</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const movies = ref([
  {
    id: 1,
    title: "Movie 1",
    poster: "https://upload.wikimedia.org/wikipedia/ko/0/02/%EC%9D%B8%EC%82%AC%EC%9D%B4%EB%93%9C_%EC%95%84%EC%9B%83_2_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg",
  },
  {
    id: 2,
    title: "Movie 2",
    poster: "https://cdn-dantats.stunning.kr/prod/portfolios/dfab4ac1-c0db-406b-962c-59c3b9fd45c5/contents/HwiHNxqZ8EJNtgPX.%EB%AA%A8%EC%85%98%EB%94%94%EC%9E%90%EC%9D%B8%20%EA%B3%BC%EC%A0%9C7%20%EC%B5%9C%EC%A2%85%EC%88%98%EC%A0%95.jpg.small?q=80&f=webp&t=crop&s=1754x2480",
  },
  {
    id: 3,
    title: "Movie 3",
    poster: "https://mblogthumb-phinf.pstatic.net/MjAxODAxMThfMjE5/MDAxNTE2MjU2NDE5MDU5.hX87C0A0-vcVa5-ME4cVapSnPYVmyAzCXmmyt_NqU7kg.Yy9RLihdKLVIL7Jl7h5p1UpFRBtJBbx3-IKVpxN6UjEg.JPEG.mrnobody0987/%EB%9D%BC%EB%9D%BC%EB%9E%9C%EB%93%9C.jpg?type=w800",
  },
  {
    id: 4,
    title: "Movie 4",
    poster: "https://design.co.kr/wp-content/uploads/2024/03/07_%ED%8C%8C%EB%AC%98_%EC%8A%A4%ED%8E%98%EC%85%9C-%ED%8F%AC%EC%8A%A4%ED%84%B0_%EC%A0%84%EB%8B%AC%EC%9A%A9-832x1189.jpg",
  },
  {
    id: 5,
    title: "Movie 5",
    poster: "https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/201602/19/htm_20160219171437117902.jpg",
  },
]);

const currentIndex = ref(2); // 초기 중앙 인덱스
const isDragging = ref(false);
const startX = ref(0);

const getStyle = (index) => {
  const offset = index - currentIndex.value;
  return {
    zIndex: movies.value.length - Math.abs(offset),
    transform: `
      translateX(${offset * 200}px)
      scale(${index === currentIndex.value ? 1.5 : 1})
    `,
  };
};

const startDrag = (event) => {
  isDragging.value = true;
  startX.value = event.clientX;
};

const onDrag = (event) => {
  if (!isDragging.value) return;
  const dragDistance = event.clientX - startX.value;

  if (Math.abs(dragDistance) > 100) {
    currentIndex.value =
      (currentIndex.value - Math.sign(dragDistance) + movies.value.length) %
      movies.value.length;
    startX.value = event.clientX;
  }
};

const stopDrag = () => {
  isDragging.value = false;
};

const hoverToCenter = (index) => {
  currentIndex.value = index;
};

const goToDetail = (movieId) => {
  router.push(`/movies/${movieId}`);
};

// 이전 포스터로 이동
const prevSlide = () => {
  currentIndex.value =
    (currentIndex.value - 1 + movies.value.length) % movies.value.length;
};

// 다음 포스터로 이동
const nextSlide = () => {
  currentIndex.value =
    (currentIndex.value + 1) % movies.value.length;
};
</script>

<style scoped>
  @import "@/assets/styles/components/mainBoxOfficeSlide.css";
</style>
