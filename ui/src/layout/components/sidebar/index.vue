<template>
  <div class="sidebar p-8 ">
    <div v-if="showBreadcrumb">
      <AppBreadcrumb />
    </div>
    <div v-else class="setting-title ml-4 mt-4 mb-12">
      <div style="font-size: 18px;font-weight: 600;width:200px">系统设置</div>
    </div>

    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu mode="horizontal" :default-active="activeMenu" active-text-color="#1C9985" router>
        <sidebar-item v-hasPermission="menu.meta?.permission" v-for="(menu, index) in subMenuList" :key="index"
          :menu="menu" :activeMenu="activeMenu">
        </sidebar-item>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getChildRouteListByPathAndName } from '@/router/index'
import SidebarItem from './SidebarItem.vue'
import AppBreadcrumb from './../breadcrumb/index.vue'

const route = useRoute()

const showBreadcrumb = computed(() => {
  const { meta } = route as any
  return (
    meta?.activeMenu &&
    (meta?.activeMenu.includes('dataset') || meta?.activeMenu.includes('application'))
  )
})

const subMenuList = computed(() => {
  const { meta } = route
  return getChildRouteListByPathAndName(meta.parentPath, meta.parentName)
})

const activeMenu = computed(() => {
  const { path, meta } = route
  return meta.active || path
})
</script>

<style lang="scss">
.sidebar {
  .el-menu {
    height: 100%;
    border: none;
  }
}

.setting-title {
  display: flex;
  align-items: center;
}
</style>
