<!-- SelectActorModal -->
<template>
  <div class="modal-overlay" v-if="isVisible">
    <div class="modal-content">
      <h2>배우를 선택하세요 (최대 10명)</h2>
      <div class="actors">
        <div
          v-for="actor in actors"
          :key="actor.id"
          class="actor-card"
          :class="{ selected: selectedActors.includes(actor) }"
          @click="toggleSelectActor(actor)"
        >
          <img
            :src="actor.profile_path
              ? 'https://image.tmdb.org/t/p/w200' + actor.profile_path
              : 'https://via.placeholder.com/150'"
            :alt="actor.name"
          />
          <p>{{ actor.name }}</p>
        </div>
      </div>
      <button @click="confirmSelection" :disabled="selectedActors.length === 0">
        배우 선택 완료
      </button>
      <button @click="closeModal">닫기</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isVisible: Boolean, // 모달 보이기 여부
    actors: Array, // 배우 리스트
  },
  emits: ["close", "confirm"],
  data() {
    return {
      selectedActors: [], // 선택된 배우
    };
  },
  methods: {
    toggleSelectActor(actor) {
      const index = this.selectedActors.indexOf(actor);
      if (index === -1 && this.selectedActors.length < 10) {
        this.selectedActors.push(actor);
      } else if (index !== -1) {
        this.selectedActors.splice(index, 1);
      }
    },
    confirmSelection() {
      this.$emit("confirm", this.selectedActors); // 선택된 배우 전달
    },
    closeModal() {
      this.$emit("close"); // 모달 닫기
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 80%;
  max-width: 600px;
}
.actors {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}
.actor-card {
  cursor: pointer;
  text-align: center;
  width: 100px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 5px;
}
.actor-card img {
  width: 100%;
  border-radius: 8px;
}
.actor-card.selected {
  border: 2px solid #007bff;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
