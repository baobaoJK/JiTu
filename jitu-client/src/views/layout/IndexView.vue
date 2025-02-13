<script setup lang="ts">
import { getSystemConfig } from '@/api/system'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const webTitle = computed(() => {
  return route.meta.title
})
const name = ref('')
onMounted(async () => {
  const res = await getSystemConfig()
  name.value = res.data.server.name
})
</script>
<template>
  <div id="layout">
    <el-container style="width: 100%; height: 100%">
      <el-aside class="side">
        <div class="title">{{ name }}</div>
        <el-menu :default-active="$route.path" class="menu" router>
          <el-menu-item index="/upload">
            <el-icon><UploadFilled /></el-icon>
            <span>上传图片</span>
          </el-menu-item>
          <el-menu-item index="/pic">
            <el-icon><PictureFilled /></el-icon>
            <span>我的图片</span>
          </el-menu-item>
          <el-menu-item index="/setting">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <el-row v-if="$route.path != '/pic'">
            <el-col :span="16" :offset="4">
              <div class="web-title">{{ webTitle }}</div>
            </el-col>
          </el-row>
          <div class="web-title" v-else>{{ webTitle }}</div>
        </el-header>
        <el-main style="padding: 0">
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<style scoped lang="scss">
@use '@/assets/scss/variable.scss' as *;
#layout {
  @extend %fullview;
}

.side {
  width: 250px;

  .title {
    background-color: #4b5563;
    height: 60px;
    color: white;
    font-size: 24px;
    text-align: center;
    line-height: 60px;
  }

  .menu {
    border-right: none;
  }
}

.header {
  background-color: #374151;

  .web-title {
    color: white;
    font-size: 20px;
    line-height: 60px;
  }
}
</style>
