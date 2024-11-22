<!-- ProfileReaction -->
<template>
    <div class="profile-reaction">
      <button
        :class="{ active: activeList === 'watched' }"
        @click="$emit('switchList', 'watched')"
      >
        봤어요
      </button>
      <button
        :class="{ active: activeList === 'wishlist' }"
        @click="$emit('switchList', 'wishlist')"
      >
        보고싶어요
      </button>
    </div>
  </template>
  
  <script setup>
  defineProps(["activeList"]);
  </script>