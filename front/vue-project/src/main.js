// main.js : Vue.js의 entry point(진입점) 역할을 하는 파일. 애플리케이션의 전반적인 설정과 초기화를 담당함.

// Vue.js 애플리케이션을 생성하고 설정하는 데 사용되는 함수들을 가져옴
// import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'     // Pinia 상태 영속화 플러그인
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'                                               // HTTP 요청 라이브러리 (npm install로 추가함)
// 로컬에서 작성한 파일들(앱 컴포넌트 및 라우터)을 import함
import App from './App.vue'
import router from './router'

// Vue 애플리케이션 생성 및 플러그인 등록
const app = createApp(App)
const pinia = createPinia()

// pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

// axios 글로벌 속성 추가 : Axios를 Vue 컴포넌트 내에서 this.$axios로 접근할 수 있도록 하기 위함
app.config.globalProperties.$axios = axios

// 앱 마운트 : Vue 애플리케이션을 HTML의 특정 DOM 요소(#app)에 연결하는 역할. 이후 Vue 컴포넌트들이 해당 DOM 요소 내에서 렌더링되고 상호작용할 수 있음.
app.mount('#app')
