<template>
  <div>
    <section class="bg-header">
      <div class="container">
        <div class="box1">
          <el-row class="text-center">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
              <h1 class="big-title">
                基于LLM大语言模型的开源知识库生成系统
              </h1>
              <p class="small-title">
                KB-builder是「滨电智言」的一款开源工具，由杭州电子科技大学滨江研究院自主开发完成，旨在成为企业的知识库构建中枢
              </p>
              <div class="flex-center btns">
                <el-button size="large" color="#626aef">
                  <a class="flex-center"
                    href="https://github.com/hduchat/KB-Builder/wiki/%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2">
                    <span>
                      下载安装
                    </span>
                    <span style="font-size: 14px;margin-left: 2px;" class="iconfont">
                      &#xe609;
                    </span>
                  </a>
                </el-button>
                <el-button size="large" color="#626aef">
                  <a href="https://github.com/hduchat/KB-Builder">
                    <span class="iconfont">
                      &#xe885;
                    </span>
                    <span>
                      github
                    </span>
                  </a>
                </el-button>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </section>
    <section class="carousel container">
      <div class="shadow">
        <el-carousel indicator-position="outside" height="auto">
          <el-carousel-item style="height:auto">
            <img :src="picUrls[0]" class="carousel-img" alt="">
          </el-carousel-item>
          <el-carousel-item style="height:auto">
            <img :src="picUrls[1]" class="carousel-img" alt="">
          </el-carousel-item>
          <el-carousel-item style="height:auto">
            <img :src="picUrls[2]" class="carousel-img" alt="">
          </el-carousel-item>
          <el-carousel-item style="height:auto">
            <img :src="picUrls[3]" class="carousel-img" alt="">
          </el-carousel-item>
          <el-carousel-item style="height:auto">
            <img :src="picUrls[4]" class="carousel-img" alt="">
          </el-carousel-item>
        </el-carousel>
      </div>
    </section>
    <section class="introduction-boxes">
      <div class="intro-box" :class="{ 'bg-light': !isReverse(index) }" v-for="(item, index) in introBoxes"
        :key="index">
        <div class="container">
          <el-row :gutter="10" class="align-center" :class="{ 'flex-row-reverse': isReverse(index) }">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
              <div class="flex-column">
                <h1 class="mb-16">{{ item.title }}</h1>
                <p class="text-muted">{{ item.intro }}</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
              <span class="intro-box-image">
                <el-image :src="item.url" style="height: 300px;" fit="fill" :lazy="true"></el-image>
              </span>
            </el-col>
          </el-row>
        </div>

      </div>
    </section>
  </div>
</template>

<script setup lang='ts' name=''>
const picUrls = [
  'https://pic.imgdb.cn/item/67173cbfd29ded1a8ce8b82a.jpg',
  'https://pic.imgdb.cn/item/67173cc0d29ded1a8ce8b862.png',
  'https://pic.imgdb.cn/item/67175c72d29ded1a8c1c0ce9.png',
  'https://pic.imgdb.cn/item/67175c72d29ded1a8c1c0cfa.png',
  'https://pic.imgdb.cn/item/67175c72d29ded1a8c1c0d06.png'
]
const introBoxes = [
  {
    title: '支持广泛',
    intro: '支持直接上传docx、txt、markdown、pdf格式文档。后续支持更多文本格式文件',
    url: 'https://maxkb.cn/images/%E5%BC%80%E7%AE%B1%E5%8D%B3%E7%94%A8.svg'
  }, {
    title: '模型中立',
    intro: '支持对接各种大语言模型来生成QA，包括本地私有大模型（Llama3／Qwen2等）、国内公共大模型（通义千问／智谱AI等）和国外公共大模型（OpenAI/Gemini等）',
    url: 'https://maxkb.cn/images/%E6%A8%A1%E5%9E%8B%E4%B8%AD%E7%AB%8B.svg'
  }, {
    title: '方式灵活',
    intro: '提供多种甚于R4G的文档切片(自定义/递归/自定义标识等)和多种文本清洗等R4G文档当预处理方式',
    url: 'https://maxkb.cn/images/%E7%81%B5%E6%B4%BB%E7%BC%96%E6%8E%92.svg'
  }, {
    title: '知识生成',
    intro: '将文本分片后，提供多个预置Prompt库，生成高质量的QA问答对，并提供基于QA的知识库管理功能',
    url: 'https://maxkb.cn/images/%E6%97%A0%E7%BC%9D%E5%B5%8C%E5%85%A5.svg'
  }
]
const isReverse = (index: number) => {
  return index % 2 === 0 ? false : true
}
</script>
<style lang='scss' scoped>
.bg-header {
  background: #f8f9fa url('https://maxkb.cn/images/banner-bg.svg') center bottom no-repeat;
  background-size: cover;
  padding: 180px 0 140px;
}

.box1 {


  .big-title {
    font-size: 45px !important;
    letter-spacing: 1px;
    color: #141414;
    text-align: center;
  }

  .small-title {
    color: #8d9398 !important;
    text-align: center;
    margin-top: 24px;
  }

  .btns {
    margin-top: 48px;
  }
}

.carousel {
  width: 100%;
  padding: 50px 0;
  position: relative;
  margin-top: -150px;

  .shadow {
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
    margin: 0 20px;
  }

  .carousel-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.introduction-boxes {
  .intro-box {
    display: flex;
    flex-wrap: wrap;
    padding: 50px;



    .flex-row-reverse {
      display: flex;
      flex-direction: row-reverse;
    }

    .flex-column {
      display: flex;
      flex-direction: column;

      .text-muted {
        color: #8d9398 !important;
        line-height: 22px;
      }
    }

    .align-center {
      display: flex;
      align-items: center;
    }
  }

  .bg-light {
    background-color: #f8f9fa;
  }
}


.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;

}


@media (min-width:576px) {
  .container {
    max-width: 570px;
  }
}

@media (min-width:768px) {
  .container {
    max-width: 570px;
  }
}

@media (min-width:992px) {
  .container {
    max-width: 810px;
  }
}

@media (min-width:1200px) {
  .container {
    max-width: 990px;
  }
}
</style>