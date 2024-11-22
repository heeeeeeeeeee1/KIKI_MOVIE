<!-- ProfileInfo -->
<template>
    <div>
      <h3>{{ user.nickname }}</h3>
      <p>{{ user.ageGroup }}</p>
      <p>{{ user.gender }}</p>
      <p>{{ user.email }}</p>
      <p>{{ user.bio }}</p>
    </div>
  </template>
  
  <script setup>
  defineProps(["user"]);
  </script>
  
  <style scoped>
  div {
    padding: 10px;
    background-color: #333;
    color: white;
    border-radius: 8px;
  }
  </style>
  