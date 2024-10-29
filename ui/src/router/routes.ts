import type { RouteRecordRaw } from 'vue-router'
import { Role } from '@/utils/permission/type'
import IndexLayout from '@/views/index/index.vue'
import IndexMain from '@/views/index/pages/index.vue'
import PricingMain from '@/views/index/pages/pricing.vue'

const modules: any = import.meta.glob('./modules/*.ts', { eager: true })
const rolesRoutes: RouteRecordRaw[] = [...Object.keys(modules).map((key) => modules[key].default)]

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/home',
    name: 'home',
    redirect: '/dataset',
    component: () => import('@/layout/app-layout/index.vue'),
    children: [...rolesRoutes]
  },
  {
    path: '/',
    name: 'homePage',
    component: IndexLayout,
    redirect: 'index.html',
    children: [
      {
        path: 'index.html',
        name: 'index',
        meta: { title: '首页' },
        component: IndexMain
      },
      {
        path: 'pricing.html',
        name: 'pricing',
        meta: { title: '企业版' },
        component: PricingMain
      }
    ]
  },
  {
    path: '/chat/:accessToken',
    name: 'Chat',
    component: () => import('@/views/chat/index.vue')
  },

  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login/index.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/login/register/index.vue')
  },
  {
    path: '/forgot_password',
    name: 'forgot_password',
    component: () => import('@/views/login/forgot-password/index.vue')
  },
  {
    path: '/reset_password/:code/:email',
    name: 'reset_password',
    component: () => import('@/views/login/reset-password/index.vue')
  },
  {
    path: '/:pathMatch(.*)',
    name: '404',
    component: () => import('@/views/404/index.vue')
  }
]
