<template>
  <LayoutContainer header="问答知识库生成">
    <div class="main-calc-height centered-content">
      <el-scrollbar>
        <div class="p-24">
          <h4 class="title-decoration-1 mb-16">文档处理方法二：问答生成</h4>
          <el-form ref="FormRef" :model="applicationForm" :rules="rules" label-position="top"
            require-asterisk-position="right">
            <el-form-item label="文件类型" required>
              <el-radio-group v-model="fileType" class="card__radio" @change="handleFileTypeChange">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-card shadow="never" class="mb-12 custom-card" :class="fileType === '0' ? 'active' : ''">
                      <el-radio value="0" size="large">
                        <div class="flex align-center">

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
            <el-form-item style="width:60%" label="问答生成方式" required>
              <el-radio-group v-model="qaGenerationType" @change="handleGenerationTypeChange">
                <el-radio label="0">基础生成</el-radio>
                <el-radio label="1">基于关键词的强化问答生成</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item style="width:60%" label="AI模型" prop="model_id">
              <el-select v-model="applicationForm.model_id" clearable filterable placeholder="请选择AI模型">
                <el-option-group v-for="(value, label) in modelOptions" :key="value"
                  :label="relatedObject(providerOptions, label, 'provider')?.name">
                  <el-option v-for="item in value.filter((v: any) => v.status === 'SUCCESS' && v.model_type === 'LLM')"
                    :key="item.id" :label="item.name" :value="item.id" class="flex-between">
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
            <el-form-item style="width:60%" label="关键词" prop="keyword" v-if="qaGenerationType === '1'">
              <el-input v-model="applicationForm.keyword" placeholder="请输入关键词，系统将会侧重“关键词”的内容生成更多问答对" />
            </el-form-item>
            <el-form-item style="width:60%" label="提示词" prop="cueWord">
              <el-select v-model="applicationForm.cueWord" clearable filterable placeholder="请选择提示词"
                value-key="cueWord">
                <el-option v-for="item in currentPromptGroup" :label="item.cueWord" :value="item"
                  @click="applicationForm.prompt = item.prompt" />
              </el-select>
            </el-form-item>
            <el-form-item style="width:100%" label="详细提示词" prop="prompt">
              <el-input v-model="applicationForm.prompt" clearable type="textarea"
                :disabled="applicationForm.isTextCleaning"
                placeholder="描述问答库的内容，详尽的描述将帮助AI能深入理解该问答库的内容，能更准确的检索到内容，提高该问答库的命中率。" maxlength="2048" show-word-limit
                :rows="6" @blur="applicationForm.prompt = applicationForm.prompt.trim()" />
            </el-form-item>
            <el-form-item>
              <el-checkbox class="mb-16" v-model="applicationForm.isTextCleaning"
                @change="handleTextCleaningChange">文本清洗</el-checkbox>
            </el-form-item>
          </el-form>
          <div class="text-right">
            <el-button color="#1C9985" type="primary" :disabled="loading" @click="onSubmit(FormRef)">问答文件生成</el-button>
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
import { reactive, ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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
  prompt: '几个理想的问答示例将在之后给出\n' +
    '例子:\n' +
    '[问题]: 大模型有字数限制无法大文档一次输入？\n' +
    '[回答]: 目前这个没有好的解决办法，只能通过预先拆分大文档为多个文档片段后分批执行。\n\n' +
    '[问题]: gpt两个步骤是否可以合并成一个请求让gpt返回，可以节省约一半的时间和tokens？\n' +
    '[回答]: 拆成两次主要是因为问题可能需要人工微调修改后再去生成答案，这样可以提高知识库质量，当然也可以全部自动处理。\n\n' +
    '请模仿理想问答示例的格式，问答中必须含有对应的“[问题]”和“[回答]”标签、\n\n' +
    '请着重满足以下要求\n' +
    '1: 若文本未提供完整信息，导致问答不完整，请不要生成该问答。另外，确认问答涉及多项内容时，确保完整性，若不完整则跳过。\n' +
    '2: 确保所有生成的问题和答案语法通顺，语言表达准确、无误。\n' +
    '3: 严格避免生成无意义或含糊不清的回答，关注回答是否与问题直接相关，拒绝生成与问题无关的或模糊的内容。\n' +
    '请生成尽可能多的问答来评估对以下文本的了解\n' +
    '请尽可能生成简洁准确的问题，不要以文件名称开头作为状语\n' +
    '请仅提供问答对\n\n' +
    '若提供的信息不充分请不要生成问答对\n' +
    '不要生成无意义的问答对，不要重复问题为答案，如以疑问句回答问题，不要在回答中仅仅重复问题 \n' +
    '请不要生成不正面回答问题的无意义问答对\n\n' +
    '文本：\n'
}, {
  cueWord: '文学教育Prompt模板',
  prompt: '请作为一个教育从业者针对给出的文本生成问答，用于评估学生对文本的熟悉程度\n' +
    '几个理想的文学问答示例将在之后给出\n' +
    '例子：\n' +
    '问题: 在草船借箭这一回中，谁与诸葛亮一起草船借箭？\n' +
    '回答: 是鲁肃与诸葛亮一起草船借箭。\n\n' +
    '问题: 在草船借箭这一回中，谁提出了草船借箭这一计谋？\n' +
    '回答: 是诸葛亮提出了草船借箭。\n\n' +
    '要求：\n' +
    '- 请生成尽可能多的问答来评估对学生对以下文本的了解\n' +
    '- 生成的问答请尽可能丰富\n' +
    '- 请仅提供问答\n' +
    '- 请使用通俗的语言生成问答\n\n' +
    '文本：\n'
}, {
  cueWord: '产品说明书Prompt模板',
  prompt: '请作为一个资深工程师，针对文本生成问答\n\n' +
    '几个理想的问答示例将在之后给出\n' +
    '例子：\n' +
    '问题: 阿司匹林禁用的情况有哪些？\n' +
    '回答: 禁用的情况包括活动性溃疡病或其他原因引起的消化道出血，血友病或血小板减少症，以及有阿司匹林或其他非类抗炎药过敏史者，尤其是出现哮喘、神经血管性水肿或休克者。\n\n' +
    '问题: 阿司匹林的半衰期（Ti2）是多少？\n' +
    '回答: 阿司匹林的半衰期（Ti2）为15～20分钟。\n\n' +
    '要求：' +
    '- 请详细指明问答的对象\n' +
    '- 请仅提供问答\n' +
    '- 若提供的信息不充分请不要生成问答\n' +
    '- 请生成数个总结性的问答\n' +
    '- 若文本的信息不充分请不要生成问答\n\n' +
    '文本：\n'
}])
const promptGroup_keyword = ref([{
  cueWord: '基于关键词的强化问答生成',
  prompt: '根据提供的文本内容，生成10个与之相关的问答对。每个问答对都需围绕给定的“关键词”展开，确保：\n' +
    '\n' +
    '- 问题和答案尽可能多样化，涵盖与关键词相关的各个方面。\n' +
    '- 内容丰富，使用通俗易懂的语言，确保读者能够轻松理解。\n' +
    '- 每个问答对都需要紧密围绕关键词展开，提供详细且有见地的解释或信息。\n' +
    '- 你只需要按照例子的格式输出问答对即可' +
    '\n\t例子：' +
    '\n\t问题:在草船借箭这一回中，谁与诸葛亮一起草船借箭？' +
    '\n\t回答:是鲁肃与诸葛亮一起草船借箭。' +
    '\n' +
    '\n\t问题:在草船借箭这一回中，谁提出了草船借箭这一计谋？' +
    '\n\t回答:是诸葛亮提出了草船借箭。' +
    '\n文本：'
}])

const appId = ref()
const { dataset } = useStore()
const FormRef = ref()
const AIModelArr = ref([])
const documentArr = ref<any>([])
const loading = ref(false)
const { model } = useStore()
const qaGenerationType = ref('0')
const isTextCleaning = ref(false)

const router = useRouter()
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
  isTextCleaning: false
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
const fileType = ref('0'); // 默认选择 "未处理的文件"
const handleFileTypeChange = () => {
  applicationForm.value.document_id = '';
  if (fileType.value === '0') {
    getDocuments();
  } else {
    getProcessedDocuments();
  }
};

// 不同问答生成类型的提示词获取
const currentPromptGroup = computed(() => {
  return qaGenerationType.value === '0' ? promptGroup.value : promptGroup_keyword.value;
});

// 切换生成类型后清空部分内容
const handleGenerationTypeChange = () => {
  applicationForm.value.keyword = null;
  applicationForm.value.cueWord = null;
  applicationForm.value.prompt = '';
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
      applicationForm.value.process_type = 0;  // 设置处理方式为0

      // 跳转到【结果文件】(有bug)
      // await router.push({ path: `/dataset/${id}/document` });
      // 拼接提示词
      if (qaGenerationType.value === '1' && applicationForm.value.keyword) {
        applicationForm.value.prompt =
          `关键词：${applicationForm.value.keyword.trim()}\n${applicationForm.value.prompt}`;
      }

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

const handleTextCleaningChange = () => {
  if (applicationForm.value.isTextCleaning) {
    const selectedPrompt = currentPromptGroup.value.find(
      item => item.cueWord === applicationForm.value.cueWord.cueWord
    );

    if (selectedPrompt) {
      applicationForm.value.prompt = selectedPrompt.prompt;
    }
  }
};

onMounted(() => {
  getApplicationId().then(() => {
    getModel()
  })
  handleFileTypeChange();
})


</script>

<style lang="scss" scoped>
.el-form {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;

  .el-form-item {
    width: calc(50% - 14px);
    display: flex;
    flex-direction: column;
    // align-items: center;
  }
}

.centered-content {
  // margin: 0 auto;
  width: 100%;
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