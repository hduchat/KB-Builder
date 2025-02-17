import { hasPermission } from '@/utils/permission/index'
import Layout from '@/layout/main-layout/index.vue'
import { Role } from '@/utils/permission/type'
const settingRouter = {
  path: '/setting',
  name: 'setting',
  meta: { icon: 'Setting', title: '系统设置', permission: 'SETTING:READ' },
  redirect: () => {
    if (hasPermission(new Role('ADMIN'), 'AND')) {
      return '/template'
    }
    return '/template'
  },
  component: Layout,
  children: [
    {
      path: '/template',
      name: 'template',
      meta: {
        icon: 'app-template',
        iconActive: 'app-template-active',
        title: '模型设置',
        activeMenu: '/setting',
        parentPath: '/setting',
        parentName: 'setting'
      },
      component: () => import('@/views/template/index.vue')
    }
    // {
    //   path: '/user',
    //   name: 'user',
    //   meta: {
    //     icon: 'User',
    //     iconActive: 'UserFilled',
    //     title: '用户管理',
    //     activeMenu: '/setting',
    //     parentPath: '/setting',
    //     parentName: 'setting',
    //     permission: new Role('ADMIN')
    //   },
    //   component: () => import('@/views/user-manage/index.vue')
    // },
    // {
    //   path: '/team',
    //   name: 'team',
    //   meta: {
    //     icon: 'app-team',
    //     iconActive: 'app-team-active',
    //     title: '团队成员',
    //     activeMenu: '/setting',
    //     parentPath: '/setting',
    //     parentName: 'setting'
    //   },
    //   component: () => import('@/views/team/index.vue')
    // }
  ]
}

export default settingRouter
