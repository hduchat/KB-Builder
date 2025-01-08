<script setup lang="ts">
import { TopBar, AppMain } from '../components'
</script>

<template>
  <div class="app-layout">
    <div class="app-header">
      <TopBar />
    </div>
    <div class="app-main">
      <AppMain />
    </div>
  </div>
</template>
<style lang="scss" scoped>
.app-layout {
  background-color: #FBFCFE;
  height: 100%;
  display: flex;
}

.app-header {
  border-right: 1px solid #E0E0E0;
  background: #FFF;
  width: 220px;
  height: 100%;
  z-index: 100;
}

.app-main {
  flex: 1;
  position: relative;
  height: 100%;
  padding: 40px 20px 0;
  box-sizing: border-box;
  overflow: auto;
}
</style>
