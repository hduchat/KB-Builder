<template>
  <div class="h-full detail-container">
    <div class="sidebar-container">
      <Sidebar />
    </div>
    <div class="view-container">
      <AppMain />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Sidebar, AppMain } from '../components'
</script>
<style lang="scss">
.detail-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-container {
  height: 100px;
  box-sizing: border-box;
  transition: width 0.28s;
  // width: var(--sidebar-width);
  // min-width: var(--sidebar-width);
  background-color: var(--sidebar-bg-color);
}

.view-container {
  height: calc(100% - 100px);
  // width: calc(100% - var(--sidebar-width));
}
</style>
