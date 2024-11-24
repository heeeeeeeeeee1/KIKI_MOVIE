<template>
  <div class="movie-recommendation">
    <h3>추천 영화</h3>
    <div v-if="movies.length" class="movie-list">
      <div class="movie-card" v-for="movie in movies" :key="movie.title">
        <img :src="movie.poster_path" :alt="movie.title" />
        <p>{{ movie.title }}</p>
        <p>개봉일: {{ movie.release_date }}</p>
      </div>
    </div>
    <div v-else>
      <p>추천할 영화가 없습니다.</p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "{PredictMovie}",
  props: {
    movies: {
      type: Array,
      required: true,
    },
  },
});
</script>

<style scoped>
.movie-recommendation {
  text-align: center;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.movie-card {
  width: 150px;
  margin: 10px;
  text-align: center;
}

.movie-card img {
  width: 100%;
  border-radius: 5px;
}
</style>
