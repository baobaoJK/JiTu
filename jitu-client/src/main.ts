import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Element-Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 图片查看插件
import 'viewerjs/dist/viewer.css'
import VueViewer from 'v-viewer'

app.use(VueViewer)
app.use(ElementPlus)
app.use(createPinia())
app.use(router)

app.mount('#app')
