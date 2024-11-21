<!-- MovieDetailView.vue -->
<template>
    <h1>영화 상세 정보 페이지</h1>
    <div class="movie-detail" v-if="movie">
        <!-- 좌측 영화 포스터 -->
        <img :src="movie.poster_path || '/default-poster.png'" alt="poster" />

        <!-- 우측 영화 정보 -->
        <div>
            <h1>{{ movie.title }}</h1>
            <h1>{{ movie.original_title }}</h1>
            <p>출연진: {{ movie.actors}} </p>
            <p>감독: {{ movie.directors}} </p>
            <p>장르: {{ movie.genre}} </p>
            <p>개봉일: {{ movie.release_date}} </p>
            <p>{{ movie.description }} </p>

            <!-- 인증된 사용자만 작성 가능_아직 구현 안함 -->
            <button>리뷰 남기기</button>
            <button>보고싶어요</button>
        </div>
    </div>

    <!-- 하단 리뷰 리스트 -->
    <div>
        <h3>리뷰</h3>
        <div class="reviews" v-if="reviews.length">
            <div
                v-for="review in reviews"
                :key="review.id"
                class="review-item"
            >
                <!-- SingleReview 컴포넌트 사용 -->
                <SingleReview :review="review" />
            </div>
            <!-- <SingleReview
                v-for="review in reviews"
                :key="review.id"
                :review-id="review.id"
                :review="review"
            /> -->
        </div>
        <p v-else>등록된 리뷰가 없습니다.</p>
    </div>           
    <!-- 단일 리뷰로 이동하는 링크 -->
    <!-- <router-link :to="{ name: 'SingleReview', params: { moviePk: movie.id, reviewPk: review.id } }">
    </router-link> -->
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'
import SingleReview from '@/components/SingleReview.vue'

const route = useRoute()
const movieStore = useMovieStore()
const { movie, reviews, getMovie } = movieStore

// 컴포넌트가 마운트되면 영화 데이터 로드
onMounted(() => {
    console.log("MoviePk:", route.params.moviePk); // MoviePk 값을 확인
    getMovie(route.params.moviePk); // URL의 id를 기반으로 영화 데이터 요청
})
console.log(movie)
</script>



<style scoped>

</style>