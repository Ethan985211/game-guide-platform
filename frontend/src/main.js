import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

// 将 router 暴露到全局，以便 analytics 服务使用
window.router = router

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
