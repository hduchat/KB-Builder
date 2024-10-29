<template>
  <div class="top-bar flex-between align-center">
    <a class="logo-title flex align-center" href="">
      <img class="logo" src="@/assets/logo.png" height="40" alt="">
      <div class="logo-font">KB-Builder</div>
    </a>
    <div class="top-menu-container flex align-center h-full">
      <MenuItem :menu="menu" v-for="(menu, index) in topMenuList" :key="index">
      </MenuItem>
      <div class="menu-item-container flex-center h-full">
        <a href="https://github.com/hduchat/KB-Builder/wiki">使用手册</a>
      </div>

      <el-button size="large" color="#626aef" @click.stop @click="goToLogin">
        <span>
          免费体验
        </span>
        <span style="font-size: 16px;margin-left: 2px;" class="iconfont">
          &#xe642;
        </span>
      </el-button>
    </div>

  </div>
</template>

<script setup lang='ts' name=''>
import { computed } from 'vue'
import { getChildRouteListByPathAndName } from '@/router/index'
import MenuItem from './MenuItem.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const topMenuList = computed(() => {
  return getChildRouteListByPathAndName('/', 'homePage')
})

const goToLogin = () => {
  router.push({ name: 'home' })
}
</script>
<style lang='scss' scoped>
.menu-item-container {
  margin-right: 28px;
  cursor: pointer;
  font-size: 16px;
  position: relative;
}

.top-bar {
  padding: 20px 60px;
  box-shadow: 0 0 3px rgba(60, 72, 88, 0.15);
}

.logo-title {
  display: flex;
  align-items: center;

  .logo {
    margin-right: 10px;
  }

  .logo-font {
    background: var(--app-logo-color);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: Arial Black;
    font-style: normal;
    font-weight: 900;
    font-size: 32px;
  }
}
</style>