<!-- KikiMovieView -->
<template>
  <main class="main-home-container">
    <div class="main-home">
      <!-- 애니메이션 토글 버튼 -->
      <button class="action-button" @click="toggleAnimation">
        {{ isAnimationPaused ? "시작" : "멈춤" }}
      </button>
      <div class="circle-container" :class="{ paused: isAnimationPaused }">
        <!-- 박스들 -->
        <div class="recommendation-box actor_box" title="actor">
          <RouterLink :to="{ name: 'PredictActor' }">
            <img
              src="https://img2.quasarzone.com/editor/2023/04/15/6531cd90af5bc0c06d4fd958214fdd7a.png"
              alt=""
            />
          </RouterLink>
        </div>
        <div class="recommendation-box let_box" title="dora">
          <RouterLink :to="{ name: 'RouletteView' }">
            <img
              src="https://img2.quasarzone.com/editor/2023/04/15/6531cd90af5bc0c06d4fd958214fdd7a.png"
              alt=""
            />
          </RouterLink>
        </div>
        <div class="recommendation-box office_box" title="office">
          <RouterLink :to="{ name: 'BoxOffice' }">
            <img
              src="https://img2.quasarzone.com/editor/2023/04/15/6531cd90af5bc0c06d4fd958214fdd7a.png"
              alt=""
            />
          </RouterLink>
        </div>
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
      isAnimationPaused: false,
    };
  },
  methods: {
    toggleAnimation() {
      this.isAnimationPaused = !this.isAnimationPaused;
    },
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
  padding: 20px;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  min-height: 100vh;
}

.circle-container {
  position: relative;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  animation: rotate-z 6s infinite alternate;
}

.circle-container.paused {
  animation-play-state: paused; /* 멈춘 상태 */
}
/* 박스 형태 스타일 */
.recommendation-box {
  background: #444;
  color: white;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 200px;
  height: 200px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  position: absolute;
  animation: rotate-z 6s infinite alternate;
}

@keyframes rotate-z {
  0% {
    transform: rotateZ(0deg);
  }
  20% {
    transform: rotateZ(360deg);
  }
  50% {
    transform: rotateZ(-90deg);
  }
  70% {
    transform: rotateZ(270deg);
  }
  100% {
    transform: rotateZ(0deg);
  }
}
.recommendation-box:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
.actor_box {
  top: -20%;
  left: 30%;
}

.let_box {
  top: 50%;
  right: -20%;
}

.office_box {
  bottom: 5%;
  left: -20%;
}

.recommendation-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 1rem;
}
/* 버튼 스타일 */
.main-home {
  position: relative;
}

.action-button {
  background-color: green;
  color: white;
  font-size: bold;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s;
  position: absolute;
  top: 270px;
  left: 270px;
  z-index: 999;
}

.action-button:hover {
  background-color: red;
}

.action-button {
  position: absolute;
  top: 270px;
  left: 270px;
  z-index: 999;
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
