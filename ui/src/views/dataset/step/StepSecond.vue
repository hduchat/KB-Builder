<template>  
  <div class="set-rules">  
    <el-row>  
      <el-col :span="10" class="p-24">  
        <h4 class="title-decoration-1 mb-16">设置分段规则</h4>  
        <div class="set-rules__right">  
          <el-scrollbar>  
            <div class="left-height" @click.stop>  
              <el-scrollbar>  
                <div class="scrollable-container">  
                  <el-radio-group v-model="radio" class="set-rules__radio">  
                    <!-- 智能分段 -->  
                    <el-card shadow="never" class="mb-16" :class="radio === '1' ? 'active' : ''">  
                      <el-radio value="1" size="large">  
                        <p class="mb-4">智能分段（推荐)</p>  
                        <el-text type="info">不了解如何设置分段规则推荐使用智能分段</el-text>  
                      </el-radio>  
                    </el-card>  
                    <!-- 递归分段-->  
                    <el-card shadow="never" class="mb-16" :class="radio === '2' ? 'active' : ''">  
                      <el-radio value="2" size="large">  
                        <p class="mb-4">递归分段</p>  
                        <el-text type="info">用户可根据文档规范自行设置分段长度，重叠长度</el-text>  
                      </el-radio>  
                      <el-card v-if="radio === '2'" shadow="never" class="card-never mt-16" style="margin-left: 30px">  
                        <div class="set-rules__form">  
                          <div class="form-item mb-16">  
                            <div class="title mb-8">分段长度</div>  
                            <el-slider v-model="form.limit" show-input :show-input-controls="false" :min="256" :max="2048" />  
                          </div>  
                          <div class="form-item mb-16">  
                            <div class="title mb-8">分段重叠</div>  
                            <el-slider v-model="form.overlap" show-input :show-input-controls="false" :min="128" :max="512" />  
                          </div>  
                          <div class="form-item mb-16">  
                            <div class="title mb-8">自动清洗</div>  
                            <el-switch size="small" v-model="form.with_filter" />  
                            <div style="margin-top: 4px">  
                              <el-text type="info">去掉重复多余符号空格、空行、制表符</el-text>  
                            </div>  
                          </div>  
                        </div>  
                      </el-card>  
                    </el-card>  
                    <!-- 高级分段 -->  
                    <el-card shadow="never" class="mb-16" :class="radio === '3' ? 'active' : ''">  
                      <el-radio value="3" size="large">  
                        <p class="mb-4">高级分段</p>  
                        <el-text type="info">用户可根据文档规范自行设置分段标识符、分段长度以及清洗规则</el-text>  
                      </el-radio>  
                      <el-card v-if="radio === '3'" shadow="never" class="card-never mt-16" style="margin-left: 30px">  
                        <div class="set-rules__form">  
                          <div class="form-item mb-16">  
                            <div class="title flex align-center mb-8">  
                              <span style="margin-right: 4px">分段标识</span>  
                              <el-tooltip effect="dark" content="按照所选符号先后顺序做递归分割，分割结果超出分段长度将截取至分段长度。" placement="right">  
                                <AppIcon iconName="app-warning" class="app-warning-icon"></AppIcon>  
                              </el-tooltip>  
                            </div>  
                            <div @click.stop>  
                              <el-select v-model="form.patterns" multiple allow-create default-first-option filterable  
                                placeholder="请选择">  
                                <el-option v-for="(item, index) in splitPatternList" :key="index" :label="item.key"  
                                  :value="item.value">  
                                </el-option>  
                              </el-select>  
                            </div>  
                          </div>  
                          <div class="form-item mb-16">  
                            <div class="title mb-8">分段长度</div>  
                            <el-slider v-model="form.limit" show-input :show-input-controls="false" :min="256" :max="2048" />  
                          </div>  
                          <div class="form-item mb-16">  
                            <div class="title mb-8">自动清洗</div>  
                            <el-switch size="small" v-model="form.with_filter" />  
                            <div style="margin-top: 4px">  
                              <el-text type="info">去掉重复多余符号空格、空行、制表符</el-text>  
                            </div>  
                          </div>  
                        </div>  
                      </el-card>  
                    </el-card>  
                  </el-radio-group>  
                  
                  <div class="container-wrapper">  
                    <el-checkbox v-model="useOCR" class="mb-16">使用OCR</el-checkbox>  
                    <el-checkbox v-model="Extract_pic" class="mb-16">提取图片</el-checkbox>  
                    <div style="color: gray; font-size: 12px; margin-top: -10px;">  
                      提取图片和使用OCR可能会消耗较多时间  
                    </div>  
                    <el-button @click="splitDocument" class="align-right">生成预览</el-button>  
                  </div>  
                </div>  
              </el-scrollbar>  
            </div>  
          </el-scrollbar>  
        </div>  
      </el-col>  

      <el-col :span="14" class="p-24 border-l">  
        <div v-loading="loading">  
          <h4 class="title-decoration-1 mb-8">分段预览</h4>  
          <ParagraphPreview v-model:data="paragraphList" :isConnect="checkedConnect" />  
        </div>  
      </el-col>  
    </el-row>  
  </div>  
</template>  
<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch } from 'vue'
import ParagraphPreview from '@/views/dataset/component/ParagraphPreview.vue'
import documentApi from '@/api/document'
import useStore from '@/stores'
import type { KeyValue } from '@/api/type/common'
const { dataset } = useStore()
const documentsFiles = computed(() => dataset.documentsFiles)
const splitPatternList = ref<Array<KeyValue<string, string>>>([])

const radio = ref('1')
const loading = ref(false)
const paragraphList = ref<any[]>([])
const patternLoading = ref<boolean>(false)
const checkedConnect = ref<boolean>(false)
const useOCR = ref<boolean>(false) 
const Extract_pic = ref<boolean>(false)

const firstChecked = ref(true)

const form = reactive<{
  patterns: Array<string>
  limit: number
  with_filter: boolean
  [propName: string]: any
}>({
  patterns: [],
  limit: 1024,
  overlap: 256,
  with_filter: true
})

function changeHandle(val: boolean) {//是否导入分段标题
  if (val && firstChecked.value) {
    const list = paragraphList.value
    list.map((item: any) => {
      item.content.map((v: any) => {
        v['problem_list'] = v.title.trim()
          ? [
            {
              content: v.title.trim()
            }
          ]
          : []
      })
    })
    paragraphList.value = list
    firstChecked.value = false
  }
}
function splitDocument() {
  loading.value = true//加载状态

  let fd = new FormData()
  documentsFiles.value.forEach((item) => {//遍历，添加文件到FormData
    if (item?.raw) {
      fd.append('file', item?.raw)
    }
  })

  if (radio.value === '2') {
    fd.append('patterns', 'Recursive')
    Object.keys(form).forEach((key) => {
      if (key !== 'patterns') {
        fd.append(key, form[key])
      }
    })
  }

  if (radio.value === '3') {
    Object.keys(form).forEach((key) => {
      if (key == 'patterns') {
        form.patterns.forEach((item) => fd.append('patterns', item))
      } else {
        fd.append(key, form[key])
      }
    })
  }

  if (useOCR.value) {  
    fd.append('use_ocr', 'true');   
  } else {  
    fd.append('use_ocr', 'false');   
  }  

  if (Extract_pic.value) {  
    fd.append('extract_pic', 'true');   
  } else {  
    fd.append('extract_pic', 'false');   
  }  

  fd.append('get_file_content', 'true'); 

  documentApi
    .postSplitDocument(fd)
    .then((res: any) => {
      const list = res.data
      if (checkedConnect.value) {
        list.map((item: any) => {
          item.content.map((v: any) => {
            v['problem_list'] = v.title.trim()
              ? [
                {
                  content: v.title.trim()
                }
              ]
              : []
          })
        })
      }
      paragraphList.value = list
      loading.value = false
    })
    .catch(() => {
      loading.value = false
    })
}

const initSplitPatternList = () => {
  documentApi.listSplitPattern(patternLoading).then((ok) => {
    splitPatternList.value = ok.data
  })
}

watch(radio, () => {
  if (radio.value === '3') {
    initSplitPatternList()
  }
})

onMounted(() => {
  splitDocument()
})

defineExpose({
  paragraphList,
  checkedConnect,
  useOCR,
  Extract_pic,
  documentsFiles,
  form,
  radio
})
</script>
<style scoped lang="scss">  
.container-wrapper {  
  display: flex;  
  flex-direction: column;  
  align-items: flex-start;  
}  

.align-right {  
  align-self: flex-end;  
}  

.set-rules {  
  width: 100%;  

  .left-height {  
    max-height: calc(var(--create-dataset-height) - 50px);  
    overflow-x: hidden;  
  }  

  &__radio {  
    width: 100%;  
    display: block;  

    .el-radio {  
      white-space: break-spaces;  
      width: 100%;  
      height: 100%;  
      line-height: 22px;  
      color: var(--app-text-color);  
    }  

    :deep(.el-radio__label) {  
      padding-left: 30px;  
      width: 100%;  
    }  

    :deep(.el-radio__input) {  
      position: absolute;  
      top: 16px;  
    }  

    .active {  
      border: 1px solid var(--el-color-primary);  
    }  
  }  

  &__form {  
    .title {  
      font-size: 14px;  
      font-weight: 400;  
    }  
  }  
}  
</style>  