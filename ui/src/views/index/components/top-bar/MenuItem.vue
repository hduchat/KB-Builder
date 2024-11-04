<template>
  <div class="menu-item-container flex-center h-full" :class="isActive ? 'active' : ''"
    @click="router.push({ name: menu.name })">
    <!-- <div class="icon">
      <AppIcon :iconName="menu.meta ? (menu.meta.icon as string) : '404'" />
    </div> -->
    <div>
      {{
        $te(`layout.topbar.MenuItem.${String(props.menu.name)}`)
          ? $t(`layout.topbar.MenuItem.${String(props.menu.name)}`)
          : menu.meta?.title
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
  menu: RouteRecordRaw
}>()

const isActive = computed(() => {
  const { name, meta } = route
  return (name == props.menu.name) || meta?.activeMenu == props.menu.path
})
</script>
<style lang="scss" scoped>
.menu-item-container {
  margin-right: 28px;
  cursor: pointer;
  font-size: 16px;
  position: relative;

  .icon {
    font-size: 15px;
    margin-right: 5px;
    margin-top: 2px;
  }

  &:hover {
    color: var(--el-color-primary);
  }
}

.active {
  color: var(--el-color-primary);
}
</style>
