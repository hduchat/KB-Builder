<template>
  <LayoutContainer :header="isCreate ? '创建问答库' : '上传文档'" class="create-dataset">
    <template #backButton>
      <back-button @click="back"></back-button>
    </template>
    <div class="create-dataset__main flex" v-loading="loading">
      <div class="create-dataset__component main-calc-height">
        <template v-if="active === 0">
          <StepFirst ref="StepFirstRef" />
        </template>
        <template v-else-if="active === 1">
          <StepSecond ref="StepSecondRef" />
        </template>
        <template v-else-if="active === 2">
          <ResultSuccess :data="successInfo" />
        </template>
      </div>
    </div>
    <div class="create-dataset__footer text-right border-t" v-if="active !== 2">
      <el-button @click="router.go(-1)" :disabled="loading">取消</el-button>
      <el-button @click="prev" v-if="active === 1" :disabled="loading">上一步</el-button>
      <el-button color="#1C9985" @click="next" type="primary" v-if="active === 0"
        :disabled="loading || StepFirstRef?.loading">
        创建并导入
      </el-button>
      <el-button color="#1C9985" @click="submit1" type="primary" v-if="active === 1" :disabled="loading">
        开始导入
      </el-button>
    </div>
  </LayoutContainer>
</template>
<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import StepFirst from './step/StepFirst.vue'
import StepSecond from './step/StepSecond.vue'
import ResultSuccess from './step/ResultSuccess.vue'
import datasetApi from '@/api/dataset'
import type { datasetData } from '@/api/type/dataset'
import { MsgConfirm, MsgSuccess } from '@/utils/message'
import documentApi from '@/api/document'

import useStore from '@/stores'
const { dataset, document } = useStore()
const baseInfo = computed(() => dataset.baseInfo)
const webInfo = computed(() => dataset.webInfo)
const documentsFiles = computed(() => dataset.documentsFiles)

const router = useRouter()
const route = useRoute()
const {
  params: { type },
  query: { id } // id为datasetID，有id的是上传文档
} = route
const isCreate = type === 'create'
// const steps = [
//   {
//     ref: 'StepFirstRef',
//     name: '上传文档',
//     component: StepFirst
//   },
//   {
//     ref: 'StepSecondRef',
//     name: '设置分段规则',
//     component: StepSecond
//   }
// ]

const StepFirstRef = ref()
const StepSecondRef = ref()

const loading = ref(false)
const disabled = ref(false)
const active = ref(0)
const successInfo = ref<any>(null)

async function next() {//显示组件变化，active变化
  disabled.value = true
  if (await StepFirstRef.value?.onSubmit()) {
    if (active.value++ > 2) active.value = 0
  } else {
    disabled.value = false
  }
}
const prev = () => {
  active.value = 0
}

function clearStore() {
  dataset.saveBaseInfo(null)
  dataset.saveWebInfo(null)
  dataset.saveDocumentsFile([])
}


function submit1() {
  loading.value = true
  const documents = [] as any

  let fd = new FormData()
  documentsFiles.value.forEach((item) => {//遍历，添加文件到FormData
    if (item?.raw) {
      fd.append('file', item?.raw)
    }
  })

  if (StepSecondRef.value?.radio === '2') {
    fd.append('patterns', 'Recursive')
    Object.keys(StepSecondRef.value?.form).forEach((key) => {
      if (key !== 'patterns') {
        fd.append(key, StepSecondRef.value?.form[key])
      }
    })
  }

  if (StepSecondRef.value?.radio === '3') {
    Object.keys(StepSecondRef.value?.form).forEach((key) => {
      if (key == 'patterns') {
        StepSecondRef.value?.form.patterns.forEach((item) => fd.append('patterns', item))
      } else {
        fd.append(key, StepSecondRef.value?.form[key])
      }
    })
  }


  fd.append('use_ocr', StepSecondRef.value?.useOCR ? 'true' : 'false');
  fd.append('extract_pic', StepSecondRef.value?.Extract_pic ? 'true' : 'false');


  const handleSuccess = () => {
    MsgSuccess('提交成功了');
    clearStore();
    window.location.reload(); // 在操作完成后刷新页面  
  };


  const obj = { ...baseInfo.value, } as datasetData
  if (id) { // 存在id，上传文档  
    // 跳转页面
    document.setFile(id as string, fd)

    router.push({ path: `/dataset/${id}/document` })
      .then(() => {
        // 上传文档
        document.asyncspitlDocument(document.datasetId, document.file)
          .then(handleSuccess)
          .catch(() => {
            loading.value = false
          })
      })
      .catch(() => {
        loading.value = false
      })
  } else { // 不存在id，创建新知识库
    datasetApi.postfatherDataset(obj, loading)
      .then((res) => {
        successInfo.value = res.data
        active.value = 2
        clearStore()
        // 跳转页面
        document.setFile(res.data.id as string, fd)
        router.push({ path: `/dataset/${res.data.id}/document` }) // 假设新的id存储在res.data.id
          .then(() => {
            // 上传文档
            document.asyncspitlDocument(document.datasetId, document.file)
          })
          .catch(() => {
            loading.value = false
          })
      })
      .catch(() => {
        loading.value = false
      })
  }

}

function back() {
  if (baseInfo.value || webInfo.value || documentsFiles.value?.length > 0) {
    MsgConfirm(`提示`, `当前的更改尚未保存，确认退出吗?`, {
      confirmButtonText: '确认',
      type: 'warning'
    })
      .then(() => {
        router.go(-1)
        clearStore()
      })
      .catch(() => { })
  } else {
    router.go(-1)
  }
}
onUnmounted(() => {
  clearStore()
})
</script>
<style lang="scss" scoped>
.create-dataset {
  &__steps {
    min-width: 450px;
    max-width: 800px;
    width: 80%;
    margin: 0 auto;
    padding-right: 60px;

    :deep(.el-step__line) {
      left: 64% !important;
      right: -33% !important;
    }
  }

  &__component {
    width: 100%;
    margin: 0 auto;
    overflow: hidden;
  }

  &__footer {
    padding: 16px 24px;
    position: fixed;
    bottom: 0;
    left: 0;
    background: #ffffff;
    width: 100%;
    box-sizing: border-box;
  }
}
</style>
