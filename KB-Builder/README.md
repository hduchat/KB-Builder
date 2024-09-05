### 基于  LLM  大语言模型的知识库问答系统

KB Builder = Knowledge Base Builder，是一款基于  LLM  大语言模型的开源知识库生成系统。

基于 RAG（Retrieval-Augmented Generation）数据生成增强方法，平台化智能对话服务能力，提供文档知识库管理功能，支持用户上传 docx、pdf、txt、md 格式的文档；用户点击“解析文档”可调用大模型生成问答对数据，用户对生成的数据进行质量审核，筛选生成质量较好的问答对数据。

- **支持广泛**：支持直接上传文档、自动爬取在线文档（后续将会加入  PDF  文档解析功能）；
- **模型中立**：支持对接各种大语言模型，包括本地私有大模型（Llama 3 / Qwen 2  等）、国内公共大模型（通义千问  /  智谱  AI /  百度千帆  / Kimi / DeepSeek  等）和国外公共大模型（OpenAI / Azure OpenAI / Gemini  等）；
- **切片灵活**：提供多种切片方式，例如递归切片（后续将会加入  Markdown  段落切片、语义切片）；
- **QA  生成**：将文本分片后，针对每个文本生成多个问答对。

# 快速开始

---

    docker run -d --name=maxkb -p 8080:8080 -v ~/.maxkb:/var/lib/postgresql/data cr2.fit2cloud.com/1panel/maxkb

    # 用户名: admin
    # 密码: admin123.

:::
💡  可以通过源码进行安装部署
:::

# UI  展示

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/ZWGl0wXgxzKZO34Y/img/27f09b78-6937-4f48-933f-38805e71f023.png)

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/ZWGl0wXgxzKZO34Y/img/17a0ddd9-7417-48ae-bc11-1ae3bbb81796.png)

## 技术栈

- 前端：[Vue.js](https://cn.vuejs.org/)
- 后端：[Python / Django](https://www.djangoproject.com/)
- LangChain：[LangChain](https://www.langchain.com/)
- 向量数据库：[PostgreSQL / pgvector](https://www.postgresql.org/)
- 大模型：各种本地私有或者公共大模型

## 滨电智言

本项目是由++杭州电子科技大学滨江研究院++开发完成。

滨电智言是由杭州电子科技大学滨江研究院自主开发完成的面向行业细分领域的大模型产品。滨电智言强化了领域知识提取与知识构建、领域模型训练与微调、知识检索与语义匹配等能力。目前滨电智言初步构建了面向能源工业、科技教育、医疗健康垂直领域的底层模型能力，支持包括智能问答、领域内容生成、文本摘要、报告生成、数据分析等多项大模型应用能力。

滨电智言自 2023 年 8 月 31 日正式发布以来，得到腾讯网、搜狐网、杭州网和潮新闻等多家新闻媒体报道，正在和多个客户合作构建垂直行业领域大模型，力争建成高质量产学研结合垂直行业行业领域大模型，为客户打造您企业专属的行业领域大模型智能综合解决方案

# 特别鸣谢

感谢飞致云[MaxKB](https://github.com/1Panel-dev/MaxKB)项目提供的技术支持！

## License

Copyright (c) 2014-2024  飞致云  FIT2CLOUD, All rights reserved.

Licensed under The GNU General Public License version 3 (GPLv3) (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
