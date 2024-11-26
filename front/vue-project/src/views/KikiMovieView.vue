<!-- KikiMovieView -->
<template>
  <h1>추천 메인 페이지</h1>
  <main class="main-home-container">
    <div class="main-home">
      <!-- PredictActor 추천 -->
      <div class="recommendation-box">
        <RouterLink :to="{ name: 'PredictActor' }">
          <img
            src="https://img2.quasarzone.com/editor/2023/04/15/6531cd90af5bc0c06d4fd958214fdd7a.png"
            alt=""
          />
        </RouterLink>
      </div>

      <!-- 룰렛 -->
      <div class="recommendation-box">
        <RouterLink :to="{ name: 'RouletteView' }">
          <img
            src="https://img2.quasarzone.com/editor/2023/04/15/6531cd90af5bc0c06d4fd958214fdd7a.png"
            alt=""
          />
        </RouterLink>
      </div>

      <!-- 박스오피스 -->
      <div class="recommendation-box">
        <RouterLink :to="{ name: 'BoxOffice' }">
          <img
            src="https://img2.quasarzone.com/editor/2023/04/15/6531cd90af5bc0c06d4fd958214fdd7a.png"
            alt=""
          />
        </RouterLink>
      </div>
    </div>
  </main>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "KikiMovieView",
  data() {
    return {
      isActorModalVisible: false,
      isMovieModalVisible: false,
      actors: [], // 배우 목록 데이터
      movies: [], // 추천 영화 데이터
    };
  },
  methods: {
    openActorModal() {
      this.isActorModalVisible = true;
    },
    closeActorModal() {
      this.isActorModalVisible = false;
    },
    closeMovieModal() {
      this.isMovieModalVisible = false;
    },
    handleActorSelection(selectedActor) {
      console.log("선택된 배우:", selectedActor);
      this.isActorModalVisible = false;
      this.isMovieModalVisible = true; // 영화 추천 모달 표시
    },
  },
});
</script>

<style scoped>
/* 메인 컨테이너 스타일 */
.main-home-container {
  background-color: #282c34;
  padding: 20px;
  color: white;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

/* 박스 형태 스타일 */
.recommendation-box {
  background: #444;
  color: white;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 300px;
  height: 300px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.recommendation-box:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.recommendation-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 1rem;
}
/* 버튼 스타일 */
.action-button {
  background-color: #61dafb;
  color: black;
  border: none;
  padding: 10px 15px;
  margin-top: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #21a1f1;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .main-home-container {
    flex-direction: column;
    align-items: center;
  }

  .recommendation-box {
    width: 100%;
    max-width: 400px;
  }
}
</style>
