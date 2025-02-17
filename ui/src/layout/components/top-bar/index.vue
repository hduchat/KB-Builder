·
<template>
  <div class="top-bar-container">
    <div class="app-title-container flex-center cursor" @click="router.push('/')">
      <div class="app-title-icon"></div>
      <div class="app-title-text app-logo-font ml-4">
        {{ defaultTitle }}
      </div>
    </div>
    <div class="menu">
      <TopMenu></TopMenu>
    </div>
    <div class="info flex-center avatar">
      <el-tooltip effect="dark" :content="$t('layout.topbar.github')" placement="top">
        <AppIcon iconName="app-github" class="cursor color-secondary mr-8 ml-8" style="font-size: 20px"
          @click="toUrl('https://github.com/hduchat/KB-Builder')"></AppIcon>
      </el-tooltip>
      <el-tooltip effect="dark" :content="$t('layout.topbar.wiki')" placement="top">
        <AppIcon iconName="app-reading" class="cursor color-secondary mr-8 ml-8" style="font-size: 20px"
          @click="toUrl('https://github.com/hduchat/KB-Builder/wiki/%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D')"></AppIcon>
      </el-tooltip>
      <el-tooltip effect="dark" :content="$t('layout.topbar.forum')" placement="top">
        <AppIcon iconName="app-help" class="cursor color-secondary mr-16 ml-8" style="font-size: 20px"
          @click="toUrl('https://github.com/hduchat/KB-Builder/wiki')"></AppIcon>
      </el-tooltip>
      <Avatar></Avatar>
    </div>
  </div>
</template>
<script setup lang="ts">
import TopMenu from './top-menu/index.vue'
import Avatar from './avatar/index.vue'
import { useRouter } from 'vue-router'
import { langList } from '@/locales/index'
import { useLocale } from '@/locales/useLocale'
const router = useRouter()
const defaultTitle = import.meta.env.VITE_APP_TITLE

const { changeLocale } = useLocale()
const changeLang = (lang: string) => {
  changeLocale(lang)
}
function toUrl(url: string) {
  window.open(url, '_blank')
}
</script>
<style lang="scss">
.top-bar-container {
  height: 100%;
  width: 100%;
  padding: 12px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;

  .app-title-container {
    // margin-right: 45px;
    height: 70px;

    .app-title-icon {
      background-image: url('@/assets/logo.png');
      background-size: 100% 100%;
      width: 35px;
      height: 35px;
    }

    .app-title-text {
      font-size: 24px;
    }
  }

  .menu {
    flex: 1;
  }

  .info {
    heihgt: 50px;
  }

  .line {
    height: 2em;
  }
}
</style>
