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
                <el-button size="large" color="#1C9985">
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
                <el-button size="large">
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
        </el-carousel>
      </div>
      <div class="b-video">
        <a
          href="https://www.bilibili.com/video/BV1VPpcezE5u/?spm_id_from=333.337.search-card.all.click&vd_source=4911d6ed3bdda37015ba6788ae1c1ae4">
          B站官方视频介绍
        </a>
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
import { onMounted } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter()
router.beforeEach((to, from, next) => {
  // 让页面回到顶部
  document.documentElement.scrollTop = 0;
  next();
});
const picUrls = [
  'https://pic1.imgdb.cn/item/66fa5797f21886ccc0a119d8.png',
  'https://pic1.imgdb.cn/item/677de147d0e0a243d4f19e19.png',
  'https://pic1.imgdb.cn/item/677de143d0e0a243d4f19e15.png'
]
const introBoxes = [
  {
    title: '支持广泛',
    intro: '支持直接上传docx、txt、markdown、pdf格式文档。后续支持更多文本格式文件',
    url: 'https://pic1.imgdb.cn/item/677dea72d0e0a243d4f1a025.png'
  }, {
    title: '模型中立',
    intro: '支持对接各种大语言模型来生成QA，包括本地私有大模型（Llama3／Qwen2等）、国内公共大模型（通义千问／智谱AI等）和国外公共大模型（OpenAI/Gemini等）',
    url: 'https://pic1.imgdb.cn/item/677dea73d0e0a243d4f1a029.png'
  }, {
    title: '方式灵活',
    intro: '提供多种甚于R4G的文档切片(自定义/递归/自定义标识等)和多种文本清洗等R4G文档当预处理方式',
    url: 'https://pic1.imgdb.cn/item/677dea72d0e0a243d4f1a026.png'
  }, {
    title: '知识生成',
    intro: '将文本分片后，提供多个预置Prompt库，生成高质量的QA问答对，并提供基于QA的知识库管理功能',
    url: 'https://pic1.imgdb.cn/item/677de9add0e0a243d4f19fe9.png'
  }
]
const isReverse = (index: number) => {
  return index % 2 === 0 ? false : true
}

</script>
<style lang='scss' scoped>
.bg-header {
  // background: #f8f9fa url('https://img2.baidu.com/it/u=315412614,3971635865&fm=253&fmt=auto&app=138&f=PNG?w=860&h=483') center bottom no-repeat;
  // background-size: cover;
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

  .b-video {
    color: #8d9398 !important;
    text-align: center;
    margin-top: 24px;

    a:hover {
      color: blue;
    }
  }

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