<template>
  <div class="menu-item-container" :class="isActive ? 'active' : ''" @click="router.push({ name: menu.name })">
    <div class="icon iconfont">
      {{ menu.icon }}
    </div>
    <div class="menu-title">
      {{
        menu.title
      }}
    </div>

  </div>
</template>
<script setup lang="ts">
import { useRouter, useRoute, type RouteRecordRaw } from 'vue-router'
import { computed } from 'vue'
const router = useRouter()
const route = useRoute()

const props = defineProps<{
  menu: any
}>()

const isActive = computed(() => {
  const { name, path, meta } = route
  return (name == props.menu.name && path == props.menu.path) || meta?.activeMenu == props.menu.path
})
</script>
<style lang="scss" scoped>
.menu-item-container {
  display: flex;
  align-items: center;
  padding: 0 15px;
  border-radius: 5px;
  margin-bottom: 5px;
  height: 40px;
  cursor: pointer;
  font-size: 16px;
  position: relative;

  .menu-title {
    color: #71747A;
    font-size: 14px;
  }

  .icon {
    font-size: 15px;
    margin-right: 15px;
    // margin-top: 2px;
  }

  &:hover {
    background-color: #D9DEE8;
  }
}

.active {
  background-color: #D9DEE8;
}
</style>
