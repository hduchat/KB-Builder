
<p align="center">
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/7af61641-e548-459f-b377-c71c1810e38f">
</p>

# <p align="center"><span style="font-size:20px;">基于 LLM 大语言模型的知识库问答系统</span></p>


KB Builder = Knowledge Base Builder，是一款基于 LLM 大语言模型的开源知识库生成系统。
基于RAG（Retrieval-Augmented Generation）数据生成增强方法，为用户提供基于RAG的知识增强生成和知识库快速构建能力，致力于成为企业的知识构建中枢。
提供平台化智能对话服务能力，提供文档知识库管理功能，支持用户上传docx、pdf、txt、md格式的文档；用户点击“解析文档”可调用大模型生成问答对数据，筛选生成高质量的知识库问答对数据。  

- **文件类型支持广泛**：支持直接上传docx、txt、markdown、pdf格式文档、后续将支持更多文本格式文件；
- **灵活的文档处理方式**：提供多种文档切片（智能分段 / 递归拆分 / 自定义标识拆分等）和多种文本清洗等RAG文档预处理方式；
- **大语言模型中立**：支持对接各种大语言模型来生成QA，包括本地私有大模型（Llama 3 / Qwen 2 等）、国内公共大模型（通义千问 / 智谱 AI 等）和国外公共大模型（OpenAI / Gemini 等）；
- **知识生成与管理**：提供多个预置场景Prompt库，支持生成高质量的QA问答对，支持基于QA的知识库管理功能。
  
## 快速开始
```
docker run -d --name=maxkb -p 8080:8080 -v ~/.maxkb:/var/lib/postgresql/data cr2.bindian.hdu.cn/hduchat/kbbuilder
用户名: admin
密码: admin123.
```
💡 可以通过源码进行安装部署

如你有更多问题，可以查看使用手册，或者通过issue，也欢迎加入微信群和我们交流。
- [使用手册](https://github.com/hduchat/KB-Builder/wiki/%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D)
- [建议反馈](https://github.com/hduchat/KB-Builder/issues)
- [技术交流群]https://github.com/hduchat/KB-Builder/wiki/%E8%81%94%E7%B3%BB%E6%88%91%E4%BB%AC)

## UI 展示

<table style="border-collapse: collapse; border: 1px solid black;">
  <tr>
    <td width="50%";style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/fd4078db-308b-424a-a746-543fa4b0b11f" alt=" Demo1"   /></td>
    <td width="50%";style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/9aaabd11-7550-4245-b297-8156b7a28ce0" alt=" Demo2"   /></td>
  </tr>
  <tr>
    <td width="50%";style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/c0e3ada2-58ff-4aa0-92ef-88b66bea6fe8" alt=" Demo3"   /></td>
    <td width="50%";style="padding: 5px;background-color:#fff;"><img src= "https://github.com/user-attachments/assets/cedb669f-55df-4153-b45f-eeedb87768e5" alt=" Demo4"   /></td>
  </tr>
</table>


## 技术栈
- 前端：[Vue.js](https://cn.vuejs.org/)
- 后端：[Python / Django](https://www.djangoproject.com/)
- LangChain：[LangChain](https://www.langchain.com/)
- 向量数据库：[PostgreSQL / pgvector](https://www.postgresql.org/)
- 大模型：各种本地私有或者公共大模型
  
## 滨电智言
**本项目是由杭州电子科技大学滨江研究院开发完成。**  

滨电智言是由杭州电子科技大学滨江研究院自主开发完成的面向行业细分领域的大模型产品。滨电智言强化了领域知识提取与知识构建、领域模型训练与微调、知识检索与语义匹配等能力。目前滨电智言初步构建了面向能源工业、科技教育、医疗健康垂直领域的底层模型能力，支持包括智能问答、领域内容生成、文本摘要、报告生成、数据分析等多项大模型应用能力。  
滨电智言自2023年8月31日正式发布以来，得到腾讯网、搜狐网、杭州网和潮新闻等多家新闻媒体报道，正在和多个客户合作构建垂直行业领域大模型，力争建成高质量产学研结合垂直行业行业领域大模型，为客户打造您企业专属的行业领域大模型智能综合解决方案

## 特别鸣谢
感谢飞致云[MaxKB](https://github.com/1Panel-dev/MaxKB)项目提供的技术支持！  

## License  
Copyright (c) 2014-2024 滨电智言 , All rights reserved.  

Licensed under The GNU General Public License version 3 (GPLv3)  (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<https://www.gnu.org/licenses/gpl-3.0.html>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
