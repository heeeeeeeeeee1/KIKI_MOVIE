// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// 추가함. Pinia와 Axios를 글로벌 속성으로 설정?
app.config.globalProperties.$axios = axios 