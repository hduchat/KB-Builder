·
<template>
  <div class="top-bar-container border-b flex-between">
    <div class="flex-center h-full">
      <div class="app-title-container flex-center cursor" @click="router.push('/')">
        <div class="app-title-icon"></div>
        <div class="app-title-text app-logo-font ml-4">
          {{ defaultTitle }}
        </div>
      </div>
      <TopMenu></TopMenu>
    </div>

    <div class="flex-center avatar">
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
  height: var(--app-header-height);
  box-sizing: border-box;
  padding: var(--app-header-padding);

  .app-title-container {
    margin-right: 45px;

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

  .line {
    height: 2em;
  }
}
</style>
