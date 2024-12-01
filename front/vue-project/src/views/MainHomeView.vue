<template>
  <div>
    <canvas ref="fireworksCanvas"></canvas>
    <div class="line-container" v-show="currentScreen === 1">
      <div class="line">
        <div class="ball" @animationstart="animateTexts">
          <img src="@/assets/kiki_logo.png" alt="Logo" class="logo" />
        </div>
        <p class="button blink" @click="handleButtonClick" :style="{ opacity: buttonOpacity }">
          Click me 
        </p>
        <div class="text-container">
          <div v-for="(text, index) in texts" :key="index" class="text" :class="{ animate: text.animate }">
            {{ text.content }}
          </div>
        </div>
      </div>
    </div>
    <div class="following-ball" :class="{ active: isFollowing }" :style="followingBallStyle">
      <img src="@/assets/kiki_logo.png" alt="Logo" class="logo" />
    </div>
    <a
      v-for="(box, index) in boxes"
      :key="index"
      href="#"
      class="box"
      :style="boxStyle(box)"
      @mouseenter="startBoxEffect(index)"
      @mouseleave="stopBoxEffect"
      @click.prevent="handleBoxClick(index, $event)"
      v-show="currentScreen === 2"
    >
      {{ box.text }}
    </a>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue';

export default {
  setup() {
    const fireworksCanvas = ref(null);
    const currentScreen = ref(1);
    const isFollowing = ref(false);
    const followingBallStyle = reactive({ left: '0px', top: '0px', transition: 'all 0.05s ease-out' });
    const buttonOpacity = ref(0);
    const texts = ref([
      { content: "모두를 위한", animate: false },
      { content: "재미있고 특별한 영화 추천 서비스", animate: false },
      { content: "키키무비", animate: false }
    ]);
    const boxes = reactive([
      { text: "추천1", x: 0, y: 0, opacity: 0, color: '#F5F5F5', activeColor: '#FF6B6B' },
      { text: "추천2", x: 0, y: 0, opacity: 0, color: '#F5F5F5', activeColor: '#FF6B6B' },
      { text: "추천3", x: 0, y: 0, opacity: 0, color: '#F5F5F5', activeColor: '#FF6B6B' }
    ]);

    let ctx, particles = [], boxEffectInterval;

    const animateTexts = () => {
      const duration = 2000;
      const startDelay = 200;
      const textDelay = (duration - startDelay) / texts.value.length;
      texts.value.forEach((text, index) => {
        setTimeout(() => {
          text.animate = true;
          if (index === texts.value.length - 1) {
            setTimeout(() => {
              buttonOpacity.value = 1;
            }, 500);
          }
        }, startDelay + index * textDelay);
      });
    };

    const handleButtonClick = () => {
      currentScreen.value = 2;
      const ballRect = document.querySelector('.ball').getBoundingClientRect();
      followingBallStyle.left = `${ballRect.left}px`;
      followingBallStyle.top = `${ballRect.top}px`;
      isFollowing.value = true;
      positionBoxes();
      document.addEventListener('mousemove', followMouse);
    };

    const followMouse = (e) => {
      // Removed transition to make ball movement more responsive
      followingBallStyle.transition = 'none';
      followingBallStyle.left = `${e.clientX - 35}px`;
      followingBallStyle.top = `${e.clientY - 35}px`;
      // Restore transition after movement
      setTimeout(() => {
        followingBallStyle.transition = 'all 0.05s ease-out';
      }, 0);
    };

    const positionBoxes = () => {
      const buttonRect = document.querySelector('.button').getBoundingClientRect();
      const radius = 400;
      boxes.forEach((box, index) => {
        const angle = Math.random() * 2 * Math.PI;
        const r = Math.sqrt(Math.random()) * radius;
        box.x = Math.max(0, Math.min(buttonRect.left + r * Math.cos(angle), window.innerWidth - 150));
        box.y = Math.max(0, Math.min(buttonRect.top + r * Math.sin(angle), window.innerHeight - 150));
        box.opacity = 1;
      });
    };

    const boxStyle = (box) => {
      return {
        left: `${box.x}px`,
        top: `${box.y}px`,
        opacity: box.opacity,
        backgroundColor: box.color
      };
    };

    const startBoxEffect = (index) => {
      const box = document.querySelectorAll('.box')[index];
      const rect = box.getBoundingClientRect();
      let bubbles = [];

      boxEffectInterval = setInterval(() => {
        createBubbleEffect(rect.left + rect.width / 2, rect.top + rect.height / 2, bubbles);
      }, 100);
    };

    const createBubbleEffect = (x, y, bubbles) => {
      const bubble = {
        x: x + (Math.random() * 100 - 50),
        y: y + (Math.random() * 100 - 50),
        radius: Math.random() * 5 + 2,
        opacity: 1,
        color: `rgba(200, 200, 200, ${Math.random()})`
      };
      bubbles.push(bubble);

      ctx.beginPath();
      ctx.arc(bubble.x, bubble.y, bubble.radius, 0, Math.PI * 2);
      ctx.fillStyle = bubble.color;
      ctx.globalAlpha = bubble.opacity;
      ctx.fill();

      bubbles = bubbles.filter(b => {
        b.opacity -= 0.05;
        return b.opacity > 0;
      });
    };

    const stopBoxEffect = () => {
      clearInterval(boxEffectInterval);
    };

    const handleBoxClick = (index, event) => {
      event.preventDefault(); // 기본 이벤트 방지
      boxes[index].color = boxes[index].activeColor;
    };

    const animate = () => {
      ctx.clearRect(0, 0, fireworksCanvas.value.width, fireworksCanvas.value.height);
      requestAnimationFrame(animate);
    };

    onMounted(() => {
      ctx = fireworksCanvas.value.getContext('2d');
      fireworksCanvas.value.width = window.innerWidth;
      fireworksCanvas.value.height = window.innerHeight;
      animate();

      window.addEventListener('resize', () => {
        fireworksCanvas.value.width = window.innerWidth;
        fireworksCanvas.value.height = window.innerHeight;
        if (isFollowing.value) {
          positionBoxes();
        }
      });
    });

    onUnmounted(() => {
      document.removeEventListener('mousemove', followMouse);
      window.removeEventListener('resize', () => {});
    });

    return {
      fireworksCanvas,
      currentScreen,
      isFollowing,
      followingBallStyle,
      buttonOpacity,
      texts,
      boxes,
      animateTexts,
      handleButtonClick,
      boxStyle,
      startBoxEffect,
      stopBoxEffect,
      handleBoxClick
    };
  }
};
</script>

<style scoped>
body {
  margin: 0;
  height: 100vh;
  background-color: black;
  overflow: hidden;
}

canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 90;
  pointer-events: none;
}

.line-container {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.line {
  width: 50%;
  height: 2px;
  background-color: white;
  position: relative;
}

.ball {
  width: 70px;
  height: 70px;
  background-color: #ffcb3b;
  border-radius: 50%;
  position: absolute;
  left: -35px;
  top: -34px;
  animation: rollBall 2s ease-in-out forwards;
}

.logo {
  padding-top: 10px;
  width: 70px;
  height: 60px;
  pointer-events: none; /* 로고 이미지가 클릭 이벤트를 방해하지 않도록 함 */
}

.text-container {
  position: absolute;
  top: -150px;
  left: 0;
  width: 100%;
  text-align: center;
  color: white;
  z-index: 100;
}

.text {
  font-size: 24px;
  margin-bottom: 10px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s, transform 0.5s;
}

.text.animate {
  opacity: 1;
  transform: translateY(0);
}

.button {
  position: absolute;
  right: -100px;
  top: -25px;
  padding: 10px 20px;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.5s;
}

@keyframes blink-effect {
  50% {
    opacity: 0;
  }
}

.blink {
  animation: blink-effect 2s ease-in-out 2;
}

.following-ball {
  width: 70px;
  height: 70px;
  background-color: #ffcb3b;
  border-radius: 50%;
  position: fixed;
  opacity: 0;
  pointer-events: none;
  z-index: 1000;
  transition: all 0.05s ease-out;
}

.following-ball .logo {
  pointer-events: none; /* 추가된 스타일 */
}

.following-ball.active {
  opacity: 1;
}

.box {
  position: fixed;
  width: 100px;
  height: 100px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: black;
  text-decoration: none;
  font-family: Arial, sans-serif;
  transition: all 0.3s;
  opacity: 0;
  z-index: 99;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.box:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 12px rgba(0,0,0,0.20);
}

@keyframes rollBall {
  0% {
    transform: translateX(0) rotate(0deg);
  }
  100% {
    transform: translateX(calc(200% + 200px)) rotate(360deg);
  }
}
</style>