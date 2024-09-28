<template>
  <div class="dataset-list-container p-24" style="padding-top: 16px">
    <div class="flex-between mb-16">
      <h3>问答库</h3>
      <el-input v-model="searchValue" @change="searchHandle" placeholder="按名称搜索" prefix-icon="Search" class="w-240"
        clearable />
    </div>
    <div v-loading.fullscreen.lock="paginationConfig.current_page === 1 && loading">
      <InfiniteScroll :size="datasetList.length" :total="paginationConfig.total" :page_size="paginationConfig.page_size"
        v-model:current_page="paginationConfig.current_page" @load="getList" :loading="loading">
        <el-row :gutter="15">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb-16">
            <CardAdd title="创建问答库" @click="router.push({ path: '/dataset/create' })" />
          </el-col>
          <template v-for="(item, index) in datasetList" :key="index">
            <!--             <template v-if="item.type_child === '1'"> -->
            <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb-16">
              <CardBox :title="item.name" :description="item.desc" class="cursor"
                @click="router.push({ path: `/dataset/${item.id}/document` })">
                <template #icon>
                  <AppAvatar v-if="item.type === '1'" class="mr-8 avatar-purple" shape="square" :size="32">
                    <img src="@/assets/icon_web.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                  <AppAvatar v-else class="mr-8 avatar-light" shape="square" :size="32">
                    <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                </template>
                <div class="delete-button">
                  <el-tag v-if="item.type === '0'">通用型</el-tag>
                  <el-tag class="purple-tag" v-else-if="item.type === '1'" type="warning">Web 站点</el-tag>
                </div>

                <template #footer>
                  <div class="footer-content flex-between">
                    <div>
                      <span class="bold">{{ item?.document_count || 0 }}</span>
                      文档<el-divider direction="vertical" />
                      <span class="bold">{{ numberFormat(item?.char_length) || 0 }}</span>
                      字符
                      <!--                      <el-divider direction="vertical" />-->
                      <!--                      <span class="bold">{{ item?.application_mapping_count || 0 }}</span>-->
                      <!--                      关联应用-->
                    </div>
                    <div @click.stop>
                      <el-dropdown trigger="click">
                        <el-button text @click.stop>
                          <el-icon>
                            <MoreFilled />
                          </el-icon>
                        </el-button>
                        <template #dropdown>
                          <el-dropdown-menu>
                            <el-dropdown-item icon="Refresh" @click.stop="syncDataset(item)"
                              v-if="item.type === '1'">同步</el-dropdown-item>
                            <el-dropdown-item icon="Setting"
                              @click.stop="router.push({ path: `/dataset/${item.id}/setting` })">设置</el-dropdown-item>
                            <el-dropdown-item icon="Delete" @click.stop="deleteDataset(item)">删除</el-dropdown-item>
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                    </div>
                  </div>
                </template>
              </CardBox>
            </el-col>
            <!-- </template> -->
          </template>
        </el-row>
      </InfiniteScroll>
    </div>
    <SyncWebDialog ref="SyncWebDialogRef" @refresh="refresh" />
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import SyncWebDialog from '@/views/dataset/component/SyncWebDialog.vue'
import datasetApi from '@/api/dataset'
import applicationApi from '@/api/application'
import { MsgSuccess, MsgConfirm } from '@/utils/message'
import { useRouter } from 'vue-router'
import { numberFormat } from '@/utils/utils'
const router = useRouter()

const SyncWebDialogRef = ref()
const loading = ref(false)
const datasetList = ref<any[]>([])
const paginationConfig = reactive({
  current_page: 1,
  page_size: 20,
  total: 0
})

const searchValue = ref('')

function refresh(row: any) {
  MsgSuccess('同步任务发送成功')
}

function syncDataset(row: any) {
  SyncWebDialogRef.value.open(row.id)
}

function searchHandle() {
  paginationConfig.current_page = 1
  datasetList.value = []
  getList()
}

async function deleteDataset(row:any) {  
  try {  
    // 显示确认对话框，并等待用户确认  
    await MsgConfirm(`是否删除问答库：${row.name} ?`, '', {  
      confirmButtonText: '删除',  
      confirmButtonClass: 'danger'  
    });  

    // 获取父知识库的信息  
    const fatherDataset = await datasetApi.getDatasetDetail(row.id, loading);  

    // 获取子知识库 ID  
    const childId = fatherDataset.data.child_id;  

    // 获取子知识库的信息  
    const childDataset = await datasetApi.getDatasetDetail(childId, loading);  

    // 并行删除父知识库和子知识库的应用  
    await Promise.all([  
      applicationApi.delApplication(fatherDataset.data.app_id),  
      applicationApi.delApplication(childDataset.data.app_id)  
    ]);  

    // 删除数据集并更新界面  
    await datasetApi.delDataset(row.id, loading);  
    const index = datasetList.value.findIndex(v => v.id === row.id);  
    datasetList.value.splice(index, 1);  
    MsgSuccess('删除成功');  
  } catch (error) {  
    // 捕获并处理所有异步操作中的错误  
    console.error('删除失败', error);  
  }  
}

function getList() {
  datasetApi
    .getDataset(paginationConfig, searchValue.value && { name: searchValue.value }, loading)
    .then((res) => {
      paginationConfig.total = res.data.total
      const temp = res.data.records.filter((item: any) => { return item.type_child === "1" })
      datasetList.value = [...datasetList.value, ...temp]
    })
}

onMounted(() => {
  getList()
})
</script>
<style lang="scss" scoped>
.dataset-list-container {
  .delete-button {
    position: absolute;
    right: 12px;
    top: 18px;
    height: auto;
  }

  .footer-content {
    .bold {
      color: var(--app-text-color);
    }
  }

  :deep(.el-divider__text) {
    background: var(--app-layout-bg-color);
  }
}
</style>
