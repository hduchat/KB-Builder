<template>
  <LayoutContainer header="文档结构改写">
    <div class="main-calc-height centered-content">
      <el-scrollbar>
        <div class="p-24">
          <h4 class="title-decoration-1 mb-16">文档处理方法一：文档结构改写</h4>
          <el-form ref="FormRef" :model="applicationForm" :rules="rules" label-position="top"
            require-asterisk-position="right">
            <el-form-item label="文件类型" required>
              <el-radio-group v-model="applicationForm.fileType" class="card__radio" @change="handleFileTypeChange">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-card shadow="never" class="mb-12 custom-card" :class="fileType === '0' ? 'active' : ''">
                      <el-radio value="0" size="large">
                        <div class="flex align-center">
                          <AppAvatar class="mr-8 avatar-light" shape="square" :size="32">
                            <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                          </AppAvatar>
                          <div>
                            <p class="mb-4">未处理的文件</p>
                            <el-text type="info">上传后的原始文件</el-text>
                          </div>
                        </div>
                      </el-radio>
                    </el-card>
                  </el-col>
                  <el-col :span="12">
                    <el-card shadow="never" class="mb-12 custom-card" :class="fileType === '1' ? 'active' : ''">
                      <el-radio value="1" size="large">
                        <div class="flex align-center">
                          <AppAvatar class="mr-8 avatar-purple" shape="square" :size="32">
                            <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                          </AppAvatar>
                          <div>
                            <p class="mb-4">已处理的文档</p>
                            <el-text type="info">经过处理后的结果文件</el-text>
                          </div>
                        </div>
                      </el-radio>
                    </el-card>
                  </el-col>
                </el-row>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="文档列表" prop="document_id" class="mt-8">
              <el-select v-model="applicationForm.document_id" filterable clearable placeholder="请选择文档">
                <el-option v-for="item in documentArr" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
<!--            <el-form-item label="文档(预处理后的文件）" prop="document_id">-->
<!--              <el-select v-model="applicationForm.document_id" filterable clearable placeholder="请选择文档">-->
<!--                <el-option v-for="item in documentArr" :label="item.name" :value="item.id" />-->
<!--              </el-select>-->
<!--            </el-form-item>-->
            <el-form-item label="AI模型" prop="model_id">
              <el-select v-model="applicationForm.model_id" clearable filterable placeholder="请选择AI模型">
                <el-option-group v-for="(value, label) in modelOptions" :key="value"
                  :label="relatedObject(providerOptions, label, 'provider')?.name">
                  <el-option v-for="item in value.filter((v: any) => v.status === 'SUCCESS')" :key="item.id"
                    :label="item.name" :value="item.id" class="flex-between">
                    <div class="flex">
                      <span v-html="relatedObject(providerOptions, label, 'provider')?.icon"
                        class="model-icon mr-8"></span>
                      <span>{{ item.name }}</span>
                    </div>
                    <el-icon class="check-icon" v-if="item.id === applicationForm.model_id">
                      <Check />
                    </el-icon>
                  </el-option>
                  <!-- 不可用 -->
                  <el-option v-for="item in value.filter((v: any) => v.status !== 'SUCCESS')" :key="item.id"
                    :label="item.name" :value="item.id" class="flex-between" disabled>
                    <div class="flex">
                      <span v-html="relatedObject(providerOptions, label, 'provider')?.icon"
                        class="model-icon mr-8"></span>
                      <span>{{ item.name }}</span>
                      <span class="danger">{{
                        $t('views.application.applicationForm.form.aiModel.unavailable')
                      }}</span>
                    </div>
                    <el-icon class="check-icon" v-if="item.id === applicationForm.model_id">
                      <Check />
                    </el-icon>
                  </el-option>
                </el-option-group>
                <template #footer>
                  <div class="w-full text-left cursor" @click="openCreateModel()">
                    <el-button type="primary" link>
                      <el-icon class="mr-4">
                        <Plus />
                      </el-icon>
                      {{ $t('views.application.applicationForm.form.addModel') }}
                    </el-button>
                  </div>
                </template>
              </el-select>
            </el-form-item>
            <el-form-item label="提示词" prop="cueWord">
              <el-select
                v-model="applicationForm.cueWord"
                clearable
                filterable
                placeholder="请选择提示词"
                value-key="cueWord">
                <el-option v-for="item in promptGroup" :label="item.cueWord" :value="item"
                  @click="applicationForm.prompt = item.prompt" />
              </el-select>
            </el-form-item>
            <el-form-item label="详细提示词" prop="prompt">
              <el-input v-model="applicationForm.prompt" clearable type="textarea"
                placeholder="描述问答库的内容，详尽的描述将帮助AI能深入理解该问答库的内容，能更准确的检索到内容，提高该问答库的命中率。" maxlength="2048" show-word-limit
                :rows="5" @blur="applicationForm.prompt = applicationForm.prompt.trim()" />
            </el-form-item>
          </el-form>
          <div class="text-right">
            <el-button type="primary" :disabled="loading" @click="onSubmit(FormRef)">文档结构改写</el-button>
            <el-button :disabled="loading" @click="resetForm(FormRef)">重置</el-button>
          </div>
          <!-- 添加生成状态提示 -->
          <div v-if="generating" class="generating-status mt-16">
            <el-text>
              <el-icon class="is-loading primary">
                <Loading />
              </el-icon>
              文档结构改写中，请随后跳转到“结果文件”查看生成结果
            </el-text>
          </div>
        </div>
      </el-scrollbar>
    </div>
    <!-- 添加模版 -->
    <CreateModelDialog ref="createModelRef" @submit="getModel" @change="openCreateModel($event)"></CreateModelDialog>
    <SelectProviderDialog ref="selectProviderRef" @change="openCreateModel($event)" />
  </LayoutContainer>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import CreateModelDialog from '@/views/template/component/CreateModelDialog.vue'
import SelectProviderDialog from '@/views/template/component/SelectProviderDialog.vue'
import type { Provider } from '@/api/type/model'
import { relatedObject } from '@/utils/utils'
import useStore from '@/stores'
import applicationApi from '@/api/application'
import { groupBy } from 'lodash'
import { prompts } from '@/prompts/DocRewritePrompts';

const promptGroup = ref(prompts)
const appId = ref()
const { dataset } = useStore()
const FormRef = ref()
const AIModelArr = ref([])
const documentArr = ref<any>([])
const loading = ref(false)
const { model } = useStore()
const router = useRouter();  

const route = useRoute()
const {
  params: { id }
} = route as any

const modelOptions = ref<any>(null)
const providerOptions = ref<Array<Provider>>([])
const createModelRef = ref<InstanceType<typeof CreateModelDialog>>()
const selectProviderRef = ref<InstanceType<typeof SelectProviderDialog>>()
// const modelOptions = ref<any>(null)
// const providerOptions = ref<Array<Provider>>([])
const applicationForm = ref({
  document_id: '',
  model_id: '',
  prompt: '',
  cueWord: '',
  process_type: '',
  fileType: '0'
})

const rules = reactive({
  document_id: [{ required: true, message: '请选择文档', trigger: 'blur' }],
  model_id: [{ required: true, message: '请选择AI模型', trigger: 'blur' }],
  prompt: [{ required: true, message: '请输入详细关键词', trigger: 'blur' }],
})


function getModel() {
  loading.value = true

  if (appId.value) {
    applicationApi
      .getApplicationModel(appId.value)
      .then((res: any) => {
        modelOptions.value = groupBy(res?.data, 'provider')
        loading.value = false
      })
      .catch(() => {
        loading.value = false
      })
  } else {
    model
      .asyncGetModel()
      .then((res: any) => {
        modelOptions.value = groupBy(res?.data, 'provider')
        loading.value = false
      })
      .catch(() => {
        loading.value = false
      })
  }
}
const getApplicationId = async () => {
  await dataset.asyncGetDatasetDetail(id, loading).then((res: any) => {
    appId.value = res.data.app_id

  })
}
// const onSubmit = async (form: any) => {
//   if (!form) return
//   await form.validate((valid: any, fields: any) => {
//     if (valid) {
//       dataset.asyncPostDatasetQA(id, applicationForm.value, loading).then((res: any) => {
//         console.log("res", res);
//       })
//     } else {
//       console.log('error submit!', fields)
//     }
//   })
// }
const openCreateModel = (provider?: Provider) => {
  if (provider && provider.provider) {
    createModelRef.value?.open(provider)
  } else {
    selectProviderRef.value?.open()
  }
}

// 获取上传后未处理的文档
const getDocuments = async () => {
  dataset.asyncGetDatasetDocuments(id, loading).then((res: any) => {
    documentArr.value = res.data
  })
}
// 获取已经处理过的文档
const getProcessedDocuments = async () => {
  await dataset.asyncGetDatasetDetail(id, loading).then((res: any) => {
    const childDatasetId = res.data.child_id; // 获取子知识库 ID
    if (childDatasetId) {
      dataset.asyncGetDatasetDocuments(childDatasetId, loading).then((res: any) => {
        documentArr.value = res.data; // 更新文档列表
      });
    }
  });
};
const fileType = computed(() => applicationForm.value.fileType);
const handleFileTypeChange = () => {
  applicationForm.value.document_id = '';
  if (fileType.value === '0') {
    getDocuments();
  } else {
    getProcessedDocuments();
  }
};

const resetForm = (form: any) => {
  if (!form) return
  form.resetFields()
}

const generating = ref(false); // 添加 generating 状态

const onSubmit = async (form: any) => {
  if (!form) return
  await form.validate(async (valid: any, fields: any) => {
    if (valid) {
      generating.value = true; // 设置 generating 为 true
      applicationForm.value.process_type = 1;  // 设置处理方式为1，即文档重写

      // await router.push({ path: `/dataset/${id}/document` });  // 跳转到【结果文档】界面
      dataset.asyncPostDatasetQA(id, applicationForm.value, loading)
        .then((res: any) => {
          console.log("res: ", res);
        })
        .finally(() => {
          generating.value = false; // 设置 generating 为 false
        });
    } else {
      console.log('error submit!', fields)
    }
  })
}

onMounted(() => {
  getApplicationId().then(() => {
    getModel()
  })
  handleFileTypeChange();
})

</script>

<style lang="scss" scoped>
.centered-content {
  margin: 0 auto;
  width: 70%;
}


.document-info {
  margin-bottom: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.generating-status {
  text-align: center;
}

.custom-card {
  height: 70px; // 调整卡片的高度
}

.el-form-item {
  margin-bottom: 6px;
}

</style>