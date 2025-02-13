<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { UploadFile, UploadProgressEvent } from 'element-plus'
import { ElMessage } from 'element-plus'
import { formatFileSize } from '@/utils/utils'
import { getPicCount } from '@/api/pic'
import { baseURL } from '@/api/request'

// 上传列表类型
interface UploadFileList {
  percentage: number
}

// 上传地址
const uploadURL = baseURL + '/upload'
// 图库已上传图片数量
const picCount = ref(0)
// 上传组件 Ref
const uploadRef = ref()
// 文件列表
const fileList = ref([])
// 维护正在上传的文件列表
const uploadingFiles = ref<UploadFileList[]>([])

// 一键上传
const submitUpload = (event: Event) => {
  // 取消冒泡
  event?.stopPropagation()
  if (!fileList.value.length) {
    ElMessage.warning('请先选择文件！')
    return
  }
  uploadRef.value.submit() // 调用 Upload 组件的 submit 方法
}

// 删除文件
const handleRemove = (file: UploadFile) => {
  fileList.value = fileList.value.filter((f: UploadFile) => f.uid !== file.uid)
  ElMessage.success(`删除文件 - ${file.name}`)
  // 取消上传
  uploadRef.value.abort(file)
}

// 监听上传进度
const handleProgress = (event: UploadProgressEvent, file: UploadFile) => {
  console.log(event)
  // 保留两位小数
  event.percent = Math.floor(event.percent * 100) / 100
  uploadingFiles.value[file.uid] = { percentage: event.percent }
}

// 监听上传成功，上传完成后移出列表
const handleSuccess = (response: unknown, file: UploadFile) => {
  fileList.value = fileList.value.filter((f: UploadFile) => f.uid !== file.uid)
  ElMessage({
    message: '上传成功',
    type: 'success',
    grouping: true,
  })
}

// 监听上传失败
const handleError = (err: Error | ProgressEvent, file: UploadFile) => {
  ElMessage.error(`上传失败 ${err}`)
  uploadRef.value.abort(file)
  delete uploadingFiles.value[file.uid]
}

// 监听文件状态变化
const handleChange = (file: UploadFile) => {
  uploadingFiles.value[file.uid] = { percentage: 0 }
}

// 上传检测
const beforeUpload = (file: File) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

  if (!allowedTypes.includes(file.type)) {
    ElMessage({
      message: '仅支持上传 JPG、PNG、GIF、WebP 格式的图片！',
      type: 'error',
      grouping: true,
    })
    return false // 阻止上传
  }

  return true // 允许上传
}

// 初始化
onMounted(async () => {
  const res = await getPicCount()
  picCount.value = res.data.picCount
})
</script>
<template>
  <div id="upload">
    <el-row>
      <el-col :span="16" :offset="4">
        <el-card>
          <h1 class="title">Image Upload</h1>
          <div class="tips">
            没有限制，随便上传。支持 png、jpg、gif、webp 格式的文件，本站已托管
            {{ picCount }} 张图片
          </div>
          <el-upload
            drag
            multiple
            class="upload-demo"
            list-type="picture"
            ref="uploadRef"
            v-model:file-list="fileList"
            :action="uploadURL"
            :auto-upload="false"
            :before-upload="beforeUpload"
            :on-remove="handleRemove"
            :on-success="handleSuccess"
            :on-error="handleError"
            :on-progress="handleProgress"
            :on-change="handleChange"
            accept=".png,.jpg,.jpeg,.gif,.webp"
          >
            <el-tooltip effect="dark" content="点我全部上传" placement="right">
              <el-icon class="el-icon--upload" @click="submitUpload"><upload-filled /></el-icon>
            </el-tooltip>
            <p>拖拽文件到这里，支持多文件同时上传</p>
            <p>点击上面的图片上传全部已选择文件</p>

            <template #file="{ file }">
              <div class="custom-file">
                <div class="custom-file-right">
                  <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                </div>
                <div class="custom-file-mid">
                  <div class="text">
                    <p>{{ file.name }}</p>
                    <p>{{ formatFileSize(file.size) }}-等待上传</p>
                  </div>

                  <!-- 进度条显示 -->
                  <el-progress
                    v-if="uploadingFiles[file.uid].percentage > 0"
                    :percentage="uploadingFiles[file.uid].percentage"
                    :stroke-width="6"
                  />
                </div>
                <div class="custom-file-left">
                  <el-tooltip effect="dark" content="删除图片" placement="bottom">
                    <span
                      class="remove-file"
                      @click="handleRemove(file)"
                      v-if="uploadingFiles[file.uid].percentage != 100"
                      ><el-icon><CloseBold /></el-icon></span
                  ></el-tooltip>
                </div>
              </div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<style scoped lang="scss">
@use '@/assets/scss/upload/index.scss';
</style>
