<template>
  <div class="index-layout">
    <div class="index-header">
      <TopBar />
    </div>
    <div class="index-content">
      <IndexMain />
    </div>
    <div class="index-bottom">
      <BottomBar />
    </div>
  </div>
</template>

<script setup lang='ts' name=''>
import { TopBar, IndexMain, BottomBar } from './components'
window.addEventListener('scroll', function () {
  const header = document.querySelector('.index-header')
  let scrollPosition = window.scrollY
  if (scrollPosition > 50) {
    header?.classList.add('scrolled')
  } else {
    header?.classList.remove('scrolled')
  }
})
</script>
<style scoped lang="scss">
.index-layout {
  height: 100%;

  .index-header {
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1030;
    background-color: transparent;
    transition: background-color 0.5s;
  }

  .index-header.scrolled {
    background-color: white;
  }


}
</style>