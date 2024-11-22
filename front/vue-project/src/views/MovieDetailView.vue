<template>
  <div class="movie-detail-view">
    <main class="movie-container">
      <MovieInfo />
      <ReviewList />
    </main>
  </div>
</template>

<script setup>
import MovieInfo from "@/components/movieInfo.vue";
import ReviewList from "@/components/movieReviewList.vue";
import { useMovieStore } from "@/stores/movieStore";

const movieStore = useMovieStore()

movieStore.getMovie(response.data)
console.log(movieStore.movie)

</script>

<style scoped>
.movie-detail-view {
  width: 100%;
  display: flex;
  justify-content: center;
}
.movie-container {
  width: 60%;
  margin: auto 0;
  background-color: inherit;
  color: white;
}
</style>

<!-- 아래부터는 희원 코드
<template>
    <h1>영화 상세 정보 페이지</h1>
    <div class="movie-detail" v-if="movie">
        <img :src="movie.poster_path || '/default-poster.png'" alt="poster" />

        <div>
            <h1>{{ movie.title }}</h1>
            <h1>{{ movie.original_title }}</h1>
            <p>출연진: {{ movie.actors}} </p>
            <p>감독: {{ movie.directors}} </p>
            <p>장르: {{ movie.genre}} </p>
            <p>개봉일: {{ movie.release_date}} </p>
            <p>{{ movie.description }} </p>

            <button>리뷰 남기기</button>
            <button>보고싶어요</button>
        </div>
    </div>

    <div>
        <h3>리뷰</h3>
        <div class="reviews" v-if="reviews.length">
            <div
                v-for="review in reviews"
                :key="review.id"
                class="review-item"
            >
                <SingleReview :review="review" />
            </div>
            <SingleReview
                v-for="review in reviews"
                :key="review.id"
                :review-id="review.id"
                :review="review"
            />
        </div>
        <p v-else>등록된 리뷰가 없습니다.</p>
    </div>           
    단일 리뷰로 이동하는 링크
    <router-link :to="{ name: 'SingleReview', params: { moviePk: movie.id, reviewPk: review.id } }">
    </router-link>
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
-->
