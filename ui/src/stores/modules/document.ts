import { defineStore } from 'pinia'
import documentApi from '@/api/document'
import { type Ref } from 'vue'
import paragraphApi from '@/api/paragraph'

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
  async asyncspitlDocument(
    datasetId: string, 
    data: any, 
    loading?: Ref<boolean>,
    ) {  
    try {  
      loading && (loading.value = true);  
      
      const timeout = new Promise((_, reject) =>   
        setTimeout(() => reject(new Error('Request timeout')), 60 * 60 * 1000) // 1小时超时  
      );  

      const apiCall = new Promise(async (resolve, reject) => {  
        try {  
          //获取文件名信息并创建空白文档
          data.set('get_file_content', 'false');  
          const name_res: any = await documentApi.postSplitDocument(data);  
          const name_list = name_res.data;  
          const documentsNameList = name_list.map((item: any) => ({  
            name: item.name,  
            paragraphs: item.content,  
          }));  
          const result = await documentApi.postDocument(datasetId, documentsNameList, loading); //创建空白文档

          //获取文件信息
          data.set('get_file_content', 'true');
          const res: any = await documentApi.postSplitDocument(data);  
          const list = res.data;  
          const documentsNameList1 = list.map((item: any) => ({  
            name: item.name,  
            paragraphs: item.content,  
          }));  //获取ocr或者分割后的文件内容

          //将文件信息放置到文件中
          for (let i = 0; i < documentsNameList1.length; i++) { //遍历文件名 
            const documentId = result.data[i].id;  //找到对应文件的id
            for (const item of documentsNameList1[i].paragraphs){
              paragraphApi.postParagraph(datasetId, documentId,item, loading).then((res) => {
              });
            }
          }
          
          //更新文档状态为已完成
          for (const item of result.data) {  
            await documentApi.putDocument(datasetId, item.id, { extraction_status: 1 }, loading);  
          }  

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
function len(list: any): any {
  throw new Error('Function not implemented.');
}

