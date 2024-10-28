import { defineStore } from 'pinia'
import documentApi from '@/api/document'
import { type Ref } from 'vue'

const useDocumentStore = defineStore({
  id: 'document',
  state: () => ({
    operationCompleted: false, // 用于保存操作是否结束的布尔变量  
    datasetId: '' as string, // 用于保存单个文件ID  
    file: null as FormData | null // 用于保存单个FormData对象  
  }),
  actions: {
        // 函数来更新布尔变量的值  
        setOperationCompleted(status: boolean) {  
          this.operationCompleted = status;  
        },  

        // 函数来更新 file 变量  
        setFile(id: string,fileData: FormData) { 
          this.datasetId = id;  
          this.file = fileData;  
        },  

    async asyncGetAllDocument(id: string, loading?: Ref<boolean>) {
      return new Promise((resolve, reject) => {
        documentApi
          .getAllDocument(id, loading)
          .then((res) => {
            resolve(res)
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
    async asyncPostDocument(datasetId: string, data: any, loading?: Ref<boolean>) {
      return new Promise((resolve, reject) => {
        documentApi
          .postDocument(datasetId, data, loading)
          .then((data) => {
            resolve(data)
          })
          .catch((error) => {
            reject(error)
          })
      })
    },
  //   async asyncspitlDocument(datasetId: string, data: any, loading?: Ref<boolean>) {
  //     return new Promise((resolve, reject) => {
  //       documentApi
  //       .postSplitDocument(data)
  //       .then((res: any) => {
  //         const list = res.data

  //         const documents = [] as any
  //         list.map((item: any) => {
  //           documents.push({
  //             name: item.name,
  //             paragraphs: item.content
  //           })// 将每个段落的信息推入 documents 数组  
  //         })

  //         documentApi
  //         .postDocument(datasetId, documents, loading)
  //         .then((data) => {
  //           resolve(data)
  //         })
  //         .catch((error) => {
  //           reject(error)
  //         })
  //       })
  //     })
  //   }
  // },
  async asyncspitlDocument(datasetId: string, data: any, loading?: Ref<boolean>) {  
    try {  
      loading && (loading.value = true);  
      
      const timeout = new Promise((_, reject) =>   
        setTimeout(() => reject(new Error('Request timeout')), 60 * 60 * 1000) // 1小时超时  
      );  

      const apiCall = new Promise(async (resolve, reject) => {  
        try {  
          const res: any = await documentApi.postSplitDocument(data);  
          const list = res.data;  
          const documents = list.map((item: any) => ({  
            name: item.name,  
            paragraphs: item.content,  
          }));  

          const result = await documentApi.postDocument(datasetId, documents, loading);  
         
          resolve(result);  
        } catch (error) {  
          reject(error);  
        }  
      });  

      return await Promise.race([apiCall, timeout]);  
    } catch (error) {  
      return Promise.reject(error);  
    } finally {  
      loading && (loading.value = false);  
    }  
  },  
},  
  
})

export default useDocumentStore
