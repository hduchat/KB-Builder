<template>

  <el-scrollbar>
    <div class="content-container__main">
      <slot></slot>
    </div>
  </el-scrollbar>
</template>

<script setup lang="ts">
import { computed, useSlots } from 'vue'
defineOptions({ name: 'LayoutContainer' })
const slots = useSlots()
const props = defineProps({
  header: String || null,
  backTo: String
})
const showBack = computed(() => {
  const { backTo } = props
  return backTo
})
</script>

<style lang="scss" scope>
.content-container {
  box-sizing: border-box;
  height: 100%;
  transition: 0.3s;
  padding: 0 var(--app-view-padding) var(--app-view-padding);

  .content-container__header {
    box-sizing: border-box;
    padding: 16px 0;
    flex-wrap: wrap;
  }

  .content-container__main {
    background-color: var(--app-view-bg-color);
    border-radius: 4px;
    box-sizing: border-box;
    min-width: 700px;
  }
}
</style>
