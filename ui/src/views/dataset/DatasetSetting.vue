<template>
  <LayoutContainer header="设置">
    <div class="dataset-setting main-calc-height">
      <el-scrollbar>
        <div class="p-24" v-loading="loading">
          <BaseForm ref="BaseFormRef" :data="detail" />

          <el-form ref="webFormRef" :rules="rules" :model="form" label-position="top" require-asterisk-position="right">
            <el-form-item label="本地模型" required prop="model">
              <el-select v-model="form.model" clearable filterable placeholder="请选择本地模型">
                <el-option-group v-for="(value, label) in modelOptions" :key="value"
                  :label="relatedObject(providerOptions, label, 'provider')?.name">
                  <el-option
                    v-for="item in value.filter((v: any) => v.status === 'SUCCESS' && v.model_type === 'EMBEDDING')"
                    :key="item.id" :label="item.name" :value="item" class="flex-between">
                    <div class="flex">
                      <span v-html="relatedObject(providerOptions, label, 'provider')?.icon"
                        class="model-icon mr-8"></span>
                      <span>{{ item.name }}</span>
                    </div>
                    <el-icon class="check-icon" v-if="item.id === form.model.id">
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
            <el-form-item label="问答库类型" required>
              <el-card shadow="never" class="mb-8" v-if="detail.type === '0'">
                <div class="flex align-center">
                  <AppAvatar class="mr-8 avatar-light" shape="square" :size="32">
                    <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                  <div>
                    <div>通用型</div>
                    <el-text type="info">可以通过上传文件或手动录入方式构建问答库</el-text>
                  </div>
                </div>
              </el-card>
              <el-card shadow="never" class="mb-8" v-if="detail?.type === '1'">
                <div class="flex align-center">
                  <AppAvatar class="mr-8 avatar-purple" shape="square" :size="32">
                    <img src="@/assets/icon_web.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                  <div>
                    <div>Web 站点</div>
                    <el-text type="info"> 通过网站链接同步方式构建问答库 </el-text>
                  </div>
                </div>
              </el-card>
            </el-form-item>
            <el-form-item label="Web 根地址" prop="source_url" v-if="detail.type === '1'">
              <el-input v-model="form.source_url" placeholder="请输入 Web 根地址"
                @blur="form.source_url = form.source_url.trim()" />
            </el-form-item>
            <el-form-item label="选择器" v-if="detail.type === '1'">
              <el-input v-model="form.selector" placeholder="默认为 body，可输入 .classname/#idname/tagname"
                @blur="form.selector = form.selector.trim()" />
            </el-form-item>
          </el-form>


          <!--          <el-row :gutter="12">-->
          <!--            <el-col :span="12" v-for="(item, index) in application_list" :key="index" class="mb-16">-->
          <!--              <CardCheckbox value-field="id" :data="item" v-model="application_id_list">-->
          <!--                <template #icon>-->
          <!--                  <AppAvatar v-if="isAppIcon(item?.icon)" shape="square" :size="32" style="background: none"-->
          <!--                    class="mr-12">-->
          <!--                    <img :src="item?.icon" alt="" />-->
          <!--                  </AppAvatar>-->
          <!--                  <AppAvatar v-else-if="item?.name" :name="item?.name" pinyinColor shape="square" :size="32"-->
          <!--                    class="mr-12" />-->
          <!--                </template>-->
          <!--                {{ item.name }}-->
          <!--              </CardCheckbox>-->
          <!--            </el-col>-->
          <!--          </el-row>-->

          <div class="text-right">
            <el-button @click="submit" type="primary"> 保存 </el-button>
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
import CreateModelDialog from '@/views/template/component/CreateModelDialog.vue'
import SelectProviderDialog from '@/views/template/component/SelectProviderDialog.vue'
import { ref, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import BaseForm from '@/views/dataset/component/BaseForm.vue'
import datasetApi from '@/api/dataset'
import modelApi from '@/api/model'
import applicationApi from '@/api/application'
import type { ApplicationFormType } from '@/api/type/application'
import { MsgSuccess } from '@/utils/message'
import { isAppIcon } from '@/utils/application'
import useStore from '@/stores'
import { groupBy } from 'lodash'
import { relatedObject } from '@/utils/utils'
const route = useRoute()
const {
  params: { id }
} = route as any

const providerOptions = ref<Array<Provider>>([])
const selectProviderRef = ref<InstanceType<typeof SelectProviderDialog>>()
const appId = ref()
const { dataset, model } = useStore()
const modelOptions = ref<any>(null)
const webFormRef = ref()
const BaseFormRef = ref()
const loading = ref(false)
const detail = ref<any>({})
const application_list = ref<Array<ApplicationFormType>>([])
const application_id_list = ref([])
const form = ref<any>({
  source_url: '',
  selector: '',
  model: ''
})
const createModelRef = ref<InstanceType<typeof CreateModelDialog>>()
const rules = reactive({
  source_url: [{ required: true, message: '请输入 Web 根地址', trigger: 'blur' }]
})

const openCreateModel = (provider?: Provider) => {
  if (provider && provider.provider) {
    createModelRef.value?.open(provider)
  } else {
    selectProviderRef.value?.open()
  }
}

async function submit() {
  if (await BaseFormRef.value?.validate()) {
    await webFormRef.value.validate((valid: any) => {
      if (valid) {
        loading.value = true
        console.log('form.value', form.value);

        const obj =
          detail.value.type === '1'
            ? {
              application_id_list: application_id_list.value,
              meta: form.value,
              ...BaseFormRef.value.form
            }
            : {
              application_id_list: application_id_list.value,
              ...BaseFormRef.value.form
            }
        datasetApi
          .putDataset(id, obj)
          .then((res) => {
            modelApi.postLocalModel(form.value.model).then((res) => {
              MsgSuccess('保存成功')
              loading.value = false
            })
          })
          .catch(() => {
            loading.value = false
          })
      }
    })
  }
}
const getApplicationId = async () => {
  await dataset.asyncGetDatasetDetail(id, loading).then((res: any) => {
    appId.value = res.data.app_id

  })
}

async function getDetail() {
  await dataset.asyncGetDatasetDetail(id, loading).then((res: any) => {
    detail.value = res.data
    if (detail.value.type === '1') {
      form.value = res.data.meta
    }

    application_id_list.value = res.data?.application_id_list
    datasetApi.listUsableApplication(id, loading).then((ok) => {
      application_list.value = ok.data
    })
  })
}
function getModel() {
  loading.value = true
  if (appId.value) {
    applicationApi
      .getApplicationModel(appId.value)
      .then((res: any) => {
        modelOptions.value = groupBy(res?.data, 'provider')
        console.log("modelOptions.value", modelOptions.value);

        loading.value = false
      })
      .catch((err) => {
        console.log('err', err);
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

onMounted(() => {
  getDetail().then(() => {
    getApplicationId().then(() => {
      getModel()
    })
  })
})
</script>
<style lang="scss" scoped>
.dataset-setting {
  width: 70%;
  margin: 0 auto;
}
</style>
