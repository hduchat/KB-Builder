<template>
  <el-scrollbar>
    <div class="upload-document p-24">
      <!-- 基本信息 -->
      <BaseForm ref="BaseFormRef" v-if="isCreate" />
      <el-form
        v-if="isCreate"
        ref="webFormRef"
        :rules="rules"
        :model="form"
        label-position="top"
        require-asterisk-position="right"
      >
        <el-form-item label="问答库类型" required>
          <el-radio-group v-model="form.type" class="card__radio" @change="radioChange">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card shadow="never" class="mb-16" :class="form.type === '0' ? 'active' : ''">
                  <el-radio value="0" size="large">
                    <div class="flex align-center">
                      <AppAvatar class="mr-8 avatar-light" shape="square" :size="32">
                        <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                      </AppAvatar>
                      <div>
                        <p class="mb-4">通用型</p>
                        <el-text type="info">可以通过上传文件或手动录入方式构建问答库</el-text>
                      </div>
                    </div>
                  </el-radio>
                </el-card>
              </el-col>
            </el-row>
          </el-radio-group>
        </el-form-item>
      </el-form>

      <!-- 上传文档 -->
      <UploadComponent ref="UploadComponentRef" v-if="form.type === '0'" />
    </div>
  </el-scrollbar>
</template>
<script setup lang="ts">
import { ref, onMounted, reactive, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BaseForm from '@/views/dataset/component/BaseForm.vue'
import UploadComponent from '@/views/dataset/component/UploadComponent.vue'
import { isAllPropertiesEmpty } from '@/utils/utils'
import datasetApi from '@/api/dataset'
import { MsgError, MsgSuccess } from '@/utils/message'
import useStore from '@/stores'
const { dataset } = useStore()

const route = useRoute()
const router = useRouter()
const {
  params: { type }
} = route
const isCreate = type === 'create'
const BaseFormRef = ref()
const UploadComponentRef = ref()
const webFormRef = ref()
const loading = ref(false)

const form = ref<any>({
  type: '0',
  source_url: '',
  selector: ''
})

const rules = reactive({
  source_url: [{ required: true, message: '请输入 Web 根地址', trigger: 'blur' }]
})

watch(form.value, (value) => {
  if (isAllPropertiesEmpty(value)) {
    dataset.saveWebInfo(null)
  } else {
    dataset.saveWebInfo(value)
  }
})

function radioChange() {
  dataset.saveDocumentsFile([])
  form.value.source_url = ''
  form.value.selector = ''
}

const onSubmit = async () => {
  if (isCreate) {//判断是创建知识库还是为知识库添加文件
    if (form.value.type === '0') {//判断是文件表单还是web表单
      if ((await BaseFormRef.value?.validate()) && (await UploadComponentRef.value.validate())) {//表单和上传数据有效性
        if (UploadComponentRef.value.form.fileList.length > 50) {
          MsgError('每次最多上传50个文件！')
          return false
        } else {
          /*
        stores保存数据
      */
          dataset.saveBaseInfo(BaseFormRef.value.form)
          dataset.saveDocumentsFile(UploadComponentRef.value.form.fileList)
          return true
        }
      } else {
        return false
      }
    } else {//form.value.type === '1'，文本表单
      if (await BaseFormRef.value?.validate()) {
        await webFormRef.value.validate((valid: any) => {
          if (valid) {
            const obj = { ...BaseFormRef.value.form, ...form.value }
            datasetApi.postWebDataset(obj, loading).then((res) => {
              MsgSuccess('提交成功')
              dataset.saveBaseInfo(null)
              dataset.saveWebInfo(null)
              router.push({ path: `/dataset/${res.data.id}/document` })
              //提交数据，提示，清空表单，跳转
            })
          } else {
            return false
          }
        })
      } else {
        return false
      }
    }
  } else {//非创建模式
    if (await UploadComponentRef.value.validate()) {
      /*
        stores保存数据
      */
      dataset.saveDocumentsFile(UploadComponentRef.value.form.fileList)
      return true
    } else {
      return false
    }
  }
}

onMounted(() => {})

defineExpose({
  onSubmit,
  loading
})

</script>

<style scoped lang="scss">
.upload-document {
  width: 70%;
  margin: 0 auto;
  margin-bottom: 20 px;
}
</style>
