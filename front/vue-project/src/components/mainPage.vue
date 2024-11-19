<!-- components/mainPage.vue -->
<template>
    <div v-for="movie in movies" :key="movie">
        <h1>영화 메인 페이지</h1>
        <h3>{{ movie.title }}</h3>
        <img :src="movie.posterpath" :alt="`${movie.title} 포스터`" />
        
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stroes/movieStore'
// import { onMounted } from 'vue'

const movieStore = useMovieStore()
const { movies, error, getMovieData}

// 컴포넌트 마운트 시 영화데이터 가져오기
getMovieData()
</script>

<style scoped>

</style>