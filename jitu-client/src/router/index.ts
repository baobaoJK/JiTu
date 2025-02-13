import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '@/views/IndexView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: IndexView,
    },
    {
      path: '/layout',
      name: 'layout',
      component: () => import('@/views/layout/IndexView.vue'),
      redirect: '/upload',
      children: [
        {
          path: '/upload',
          name: 'upload',
          meta: { title: '上传图片' },
          component: () => import('@/views/upload/IndexView.vue'),
        },
        {
          path: '/pic',
          name: 'pic',
          meta: { title: '我的图片' },
          component: () => import('@/views/pic/IndexView.vue'),
        },
        {
          path: '/setting',
          name: 'setting',
          meta: { title: '系统设置' },
          component: () => import('@/views/setting/IndexView.vue'),
        },
      ],
    },
  ],
})

export default router
