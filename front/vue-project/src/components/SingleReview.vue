<!-- SingleReview.vue -->
<template>
    <div class="review">
        <p>작성자: {{ review.user.username }}</p>
        <p>내용: {{ review.content}}</p>
        <!-- 좋아요, 댓글 정보(수) -->
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useMovieStore } from '@/stores/movieStore'

// 부모 컴포넌트에서 전달받은 리뷰 ID
defineProps({
  review: Object, // 부모 컴포넌트로부터 리뷰 데이터를 전달받음
})

// const reviewData = ref(null) // 단일 리뷰 데이터 상태
// const movieStore = useMovieStore()
// const { getSingleReview } = movieStore

// // 리뷰 데이터를 가져오기
// onMounted(() => {
//   const moviePk = movieStore.movies.id; // 현재 영화 ID를 가져옴
//   getSingleReview(moviePk, reviewId).then((data) => {
//     reviewData.value = data; // 리뷰 데이터 저장
//   })
// })
</script>

<style scoped>

</style>