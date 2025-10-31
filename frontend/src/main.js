import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/style.css'   // ✅ 确保引入了全局 CSS
import '@fortawesome/fontawesome-free/css/all.css'


const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// 刷新页面时恢复登录状态
import { useUserStore } from './store/userStore.js'
const userStore = useUserStore()
userStore.restore()

app.mount('#app')
