<template>
  <div>
    <section class="bg-header">
      <div class="container">
        <div class="box1">
          <el-row class="text-center">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
              <h1 class="big-title">
                KB-Builder 专业版
              </h1>
              <p class="small-title">
                KB-builder支持企业级打造面向大模型的行业垂直领域知识模型
              </p>
              <div class="flex-center btns">
                <el-button size="large" color="#626aef">
                  <a href="https://jsj.top/f/aMG6Xs">申请试用</a>
                </el-button>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </section>
    <section class="table-section">
      <div class="container" style="padding: 0 50px;">
        <h1 class="text-center mt-20 mb-24">产品版本对比</h1>
        <table class="table">
          <thead>
            <tr>
              <th></th>
              <th class="text-center">社区版</th>
              <th class="text-center blue">专业版</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in tableItems" :class="{ 'bg-color': isOdd(index) }">
              <th class="title-bg" v-if="item.row" colspan="3">{{ item.title }}</th>
              <th class="font1" v-if="!item.row">{{ item.title }}</th>
              <td class="text-center font1" v-if="!item.row && item.td1 !== 'yes'">{{ item.td1 }}</td>
              <td class="text-center" v-if="!item.row && item.td1 == 'yes'"><span style="color:#39B54A"
                  class="icon iconfont">&#xe60e;</span>
              </td>
              <td class="text-center font1" v-if="!item.row && item.td2 !== 'yes'">{{ item.td2 }}</td>
              <td class="text-center" v-if="!item.row && item.td2 == 'yes'"><span style="color:#39B54A"
                  class="icon iconfont">&#xe60e;</span>
              </td>
            </tr>
          </tbody>

        </table>
      </div>
    </section>
  </div>
</template>

<script setup lang='ts' name=''>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter()
router.beforeEach((to, from, next) => {
  // 让页面回到顶部
  document.documentElement.scrollTop = 0;
  next();
});
const tableItems = ref([
  {
    row: true,
    title: '知识库管理',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '支持的文件类型:DOCX、PDF、Makdown、TXT',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '支持web站点同步',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '自定义 Embedding 模型',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '知识库数量',
    td1: '最多支持创建5个',
    td2: 'yes'
  },
  {
    row: true,
    title: '文档分段',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '基于NLP的文本清洗',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '基础文本分段切片，如标准、递归、自定义标识等',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '通过语义切块等高级分段能力',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '基于OCR的PDF结构化处理解析',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '基于NLP的语义级高级文档优化处理',
    td1: '-',
    td2: 'yes'
  },
  {
    row: true,
    title: '大语言模型对接',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '主流的大语言模型对接',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '主流的Embedding模型对接',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '模型权限设置',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: 'Prompt定制优化',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: 'LLM选型与微调定制优化',
    td1: '-',
    td2: 'yes'
  },
  {
    row: true,
    title: '问答生成',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '问答库数量',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '文本问答生成',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '解析文件中图片、表格、公式，问答生成',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '基于RAG的问题泛化增强',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '知识库评分与测评',
    td1: '-',
    td2: 'yes'
  },
  {
    row: true,
    title: '系统管理和设置',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '用户管理',
    td1: '最多支持创建2个',
    td2: 'yes'
  },
  {
    row: false,
    title: '权限设置',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '自定义系统Logo和主题',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '开放API',
    td1: '-',
    td2: 'yes'
  },
  {
    row: true,
    title: '安装部署',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '安装包（x86，64-bit）',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '安装包（ARM，64-bit）',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '部署模式',
    td1: '单机/冷备',
    td2: '单机/冷备'
  },
  {
    row: true,
    title: '服务规格',
    td1: '',
    td2: ''
  },
  {
    row: false,
    title: '开源社区支持',
    td1: 'yes',
    td2: 'yes'
  },
  {
    row: false,
    title: '原厂企业级技术支持服务',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '基于企业需求定制开发',
    td1: '-',
    td2: 'yes'
  },
  {
    row: false,
    title: '产品价格',
    td1: '免费',
    td2: '联系销售'
  }
])

const isOdd = (index: any) => {
  return index % 2 !== 0
}
</script>
<style lang='scss' scoped>
* {
  box-sizing: border-box;
}

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

.table-section {
  padding: 50px 0;

  .table {
    width: 100%;
    margin-bottom: 1rem;
    color: #212529;
    border-collapse: collapse;
    display: table;
    text-indent: initial;
    border-spacing: 2px;
    border-color: gray;
    table-layout: fixed;

    .blue {
      color: #3370FF;
    }

    td,
    th {
      padding: 10px 0.75rem;
      /* padding: 5px 0; */
      border-top: 10px solid #ffffff;
      border-bottom: 10px solid #ffffff;
      vertical-align: top;
      text-align: left;
    }


    td {
      font-weight: 300;
      font-size: 16px;
    }

    .font1 {
      font-weight: 300;
      font-size: 15px;
      font-family: Nunito, sans-serif;
      line-height: 1.5;
      margin-bottom: 0;
    }

    .text-center {
      text-align: center;
    }

    .title-bg {
      background-color: rgb(238, 241, 251);
      border-radius: 5px;
      padding: 10px 20px;
    }

    .bg-color {
      border-radius: 5px;
      background-color: rgb(250, 251, 253);
    }


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
    max-width: 720px;
  }
}

@media (min-width:768px) {
  .container {
    max-width: 720px;
  }
}

@media (min-width:992px) {
  .container {
    max-width: 960px;
  }
}

@media (min-width:1200px) {
  .container {
    max-width: 1140px;
  }
}
</style>