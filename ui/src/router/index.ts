import { hasPermission } from '@/utils/permission/index'
import {
  createRouter,
  createWebHistory,
  type NavigationGuardNext,
  type RouteLocationNormalized,
  type RouteRecordRaw,
  type RouteRecordName
} from 'vue-router'
import useStore from '@/stores'
import { routes } from '@/router/routes'
import datasetApi from '@/api/dataset'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

// 路由前置拦截器
router.beforeEach(
  async (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    if (to.name === '404') {
      next()
      return
    }
    const { user } = useStore()

    const notAuthRouteNameList = [
      'register',
      'login',
      'forgot_password',
      'reset_password',
      'Chat',
      'homePage',
      'index',
      'pricing'
    ]

    if (!notAuthRouteNameList.includes(to.name ? to.name.toString() : '')) {
      const token = user.getToken()
      if (!token) {
        next({
          path: '/login'
        })
        return
      } else {
        if (!user.userInfo) {
          await user.profile()
        }
        if (to.path.startsWith('/dataset/')) {
          if (to.path.startsWith('/dataset/create') || to.path.startsWith('/dataset/upload')) {
            next()
          }
          const id = to.params.id || to.query.id // 注意：在子路由中，id可能不在to.params中，而是需要通过to.params.$routeMatch或其他方式获取
          const documentId = to.params.documentId || to.query.documentId
          if (!id) {
            // 如果没有id，则重定向或显示错误
            next({ path: '/error', query: { error: 'Missing ID' } })
            return
          }

          try {
            // 发送API请求来检查id
            const response = await datasetApi.getDatasetDetail(id as string)
            if (response.data.type_child !== '1') {
              // 如果type_child不等于1，但documentId存在的话则放行
              if (documentId) {
                next()
              }
              // 如果type_child不等于1，其余情况则重定向或显示错误
              next({ path: '/error', query: { error: 'Invalid ID' } })
            } else {
              // 如果type_child等于1，则继续路由导航
              next()
            }
          } catch (error) {
            // 如果API请求失败，则处理错误
            console.error('Error fetching data for route guard:', error)
            next({ path: '/error', query: { error: 'Failed to fetch data' } })
          }
        } else {
          // 如果不是/dataset/:id的路由，则直接放行
          next()
        }
      }
    }
    // 判断是否有菜单权限
    if (to.meta.permission ? hasPermission(to.meta.permission as any, 'OR') : true) {
      next()
    } else {
      // 如果没有权限则直接取404页面
      next('404')
    }
  }
)

export const getChildRouteListByPathAndName = (path: any, name?: RouteRecordName | any) => {
  return getChildRouteList(routes, path, name)
}

export const getChildRouteList: (
  routeList: Array<RouteRecordRaw>,
  path: string,
  name?: RouteRecordName | null | undefined
) => Array<RouteRecordRaw> = (routeList, path, name) => {
  for (let index = 0; index < routeList.length; index++) {
    const route = routeList[index]
    if (name === route.name && path === route.path) {
      return route.children || []
    }
    if (route.children && route.children.length > 0) {
      const result = getChildRouteList(route.children, path, name)
      if (result && result?.length > 0) {
        return result
      }
    }
  }
  return []
}

export default router
