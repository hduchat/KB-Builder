<template>
  <div class="bottom-bar">
    <div class="footer-container">
      <div class="navigation">
        <div class="name">BDChat 滨电智言</div>
      </div>
      <div class="core_value">
        Knowledge Base Builder，是一款基于LLM大语言模型的开源知识库生成管理优化构建系统，是「滨电智言」的一款开源工具，旨在成为企业的知识库构建中枢。
      </div>
      <p class="text-light mt-20">联系电话：15702420327</p>
      <div class="line"></div>
      <div class="license">

        <p>
          <a href="https://github.com/hduchat/KB-Builder/wiki/%E4%BA%A7%E5%93%81%E8%BF%AD%E4%BB%A3">产品迭代</a>|
          <a href="https://github.com/hduchat/KB-Builder/issues">问题反馈</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang='ts' name=''>

</script>
<style lang='scss' scoped>
body {
  margin: 0;
  font-family: source-han-sans-simplified-c, open sans, Helvetica, Arial, sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  text-align: left;
  background-color: #fff;
}

.bottom-bar {
  background: #161618;
  padding: 64px 0;

  .footer-container {
    max-width: 1128px;
    margin: 0 auto;

    .navigation {
      color: #ffffff;
      display: flex;
      justify-content: space-between;

      .name {
        color: #f8f9fc;
        font-size: 20px;
        letter-spacing: 2px;
        font-weight: 800;
      }

      .links {
        justify-content: space-between;
        align-items: center;
        display: flex;
        gap: 32px;
      }
    }

    .core_value {
      width: 350px;
      color: #adb5bd;
      font-size: 15px;
      line-height: 1.5;
      font-weight: 300;
      margin-top: 10px;
    }

    .text-light {
      color: #f8f9fa !important;
    }

    .line {
      border-top: 1px solid rgba(243, 229, 200, 0.26);
      margin: 24px 0;
    }

    .license {
      p {
        color: #adb5bd;
        font-weight: 300;
        font-size: 15px;
        font-family: 'Source Han Sans SC', 'Noto Sans CJK SC', 'Source Han Sans CN', 'Noto Sans SC', 'Source Han Sans TC', 'Noto Sans CJK TC', sans-serif;
        text-align: center;
        padding: 0 12px;
        margin: 0;
        line-height: 30px;
      }
    }
  }
}
</style>