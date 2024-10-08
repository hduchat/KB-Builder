<template>
  <LayoutContainer header="问答知识库生成">
    <div class="main-calc-height centered-content">
      <el-scrollbar>
        <div class="p-24">
          <h4 class="title-decoration-1 mb-16">文档处理方法二：问答生成</h4>
          <el-form ref="FormRef" :model="applicationForm" :rules="rules" label-position="top"
            require-asterisk-position="right">
            <el-form-item label="文档(预处理后的文件)" prop="document_id">
              <el-select v-model="applicationForm.document_id" filterable clearable placeholder="请选择文档">
                <el-option v-for="item in documentArr" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
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
                :rows="6" @blur="applicationForm.prompt = applicationForm.prompt.trim()" />
            </el-form-item>
          </el-form>
          <div class="text-right">
            <el-button type="primary" :disabled="loading" @click="onSubmit(FormRef)">问答文件生成</el-button>
            <el-button :disabled="loading" @click="resetForm(FormRef)">重置</el-button>
          </div>
          <!-- 添加生成状态提示 -->
          <div v-if="generating" class="generating-status mt-16">
            <el-text>
              <el-icon class="is-loading primary">
                <Loading />
              </el-icon>
              问答正在生成中，请随后跳转到“结果文件”查看生成结果

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
import { reactive, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import type { ApplicationFormType } from '@/api/type/application'
import CreateModelDialog from '@/views/template/component/CreateModelDialog.vue'
import SelectProviderDialog from '@/views/template/component/SelectProviderDialog.vue'
import type { Provider } from '@/api/type/model'
import { relatedObject } from '@/utils/utils'
import useStore from '@/stores'
import { t } from '@/locales'
import applicationApi from '@/api/application'
import { groupBy } from 'lodash'
import datasetApi from '@/api/dataset'

const promptGroup = ref([{
  cueWord: '通用prompt模板 ',
  prompt: '几个理想的问答示例将在之后给出\n\t例子:\n\t问题：大模型有字数限制无法大文档一次输入？\n\t回答：目前这个没有好的解决办法，只能通过预先拆分大文档为多个文档片段后分批执行。\n\n\t问题：gpt两个步骤是否可以合并成一个请求让gpt返回，可以节省约一半的时间和tokens？\n\t回答：拆成两次主要是因为问题可能需要人工微调修改后再去生成答案，这样可以提高知识库质量，当然也可以全部自动处理。\n\n\t请仅提供问答\n\t若文本提供的信息不充分请不要生成相应问答\n\t请生成尽可能多的问答\n\n\t文本：\n'
}, {
  cueWord: '文学教育Prompt模板',
  prompt: '请作为一个教育从业者针对给出的文本生成问答，用于评估学生对文本的熟悉程度\n\t几个理想的文学问答示例将在之后给出\n\t例子：  \n\t问题:在草船借箭这一回中，谁与诸葛亮一起草船借箭？\n\t回答:是鲁肃与诸葛亮一起草船借箭。\n\n\t问题:在草船借箭这一回中，谁提出了草船借箭这一计谋？\n\t回答:是诸葛亮提出了草船借箭。\n\n\t请生成尽可能多的问答来评估对学生对以下文本的了解\n\t生成的问答请尽可能丰富\n\t请仅提供问答\n\t请使用通俗的语言生成问答\n\n\t文本：\n'
},
{
  cueWord: '产品说明书Prompt模板',
  prompt: '请作为一个资深工程师，针对文本生成问答\n\n\t几个理想的问答示例将在之后给出\n\t例子： \n\t问题:阿司匹林禁用的情况有哪些？\n\t回答:禁用的情况包括活动性溃疡病或其他原因引起的消化道出血，血友病或血小板减少症，以及有阿司匹林或其他非类抗炎药过敏史者，尤其是出现哮喘、神经血管性水肿或休克者。\n\n\t问题:阿司匹林的半衰期（Ti2）是多少？\n\t回答:阿司匹林的半衰期（Ti2）为15～20分钟。\n\n\t请详细指明问答的对象\n\t请仅提供问答\n\t若提供的信息不充分请不要生成问答\n\t请生成数个总结性的问答\n\t若文本的信息不充分请不要生成问答\n\n\t文本：\n'
}])
const appId = ref()
const { dataset } = useStore()
const FormRef = ref()
const AIModelArr = ref([])
const documentArr = ref<any>([])
const loading = ref(false)
const { model } = useStore()

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
const getDocuments = async () => {
  dataset.asyncGetDatasetDocuments(id, loading).then((res: any) => {
    documentArr.value = res.data
  })
}
const resetForm = (form: any) => {
  if (!form) return
  form.resetFields()
}

const generating = ref(false); // 添加 generating 状态

const onSubmit = async (form: any) => {
  if (!form) return
  await form.validate((valid: any, fields: any) => {
    if (valid) {
      generating.value = true; // 设置 generating 为 true
      applicationForm.value.process_type = 0;  // 设置处理方式为0
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
  getDocuments()
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
</style>