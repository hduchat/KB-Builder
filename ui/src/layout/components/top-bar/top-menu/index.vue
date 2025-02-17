<template>
  <div class="top-menu-container  h-full">
    <MenuItem :menu="menu" v-for="(menu, index) in topMenuList" :key="index">
    </MenuItem>
  </div>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { getChildRouteListByPathAndName } from '@/router/index'
import MenuItem from './MenuItem.vue'

const topMenuList = [{
  title: '问答库',
  name: 'dataset',
  icon: '\ue600',
  path: '/dataset'
}, {
  title: '系统设置',
  name: 'setting',
  icon: '\ue72d',
  path: '/setting'
}]
</script>
<style lang="scss" scoped>
.top-menu-container {
  display: flex;
  flex-direction: column;
}
</style>
