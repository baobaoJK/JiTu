<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import {
  getPicList,
  addPicFolder,
  getPicFolderList,
  editPicFolder,
  deletePicFolder,
  movePicService,
} from '@/api/pic'
import { ElMessage, ElMessageBox } from 'element-plus'
import ContextMenu from '@/components/ContextMenu.vue'
import type { PicFolder } from '@/model/picFolder'
import type { PicImages } from '@/model/pic'
import SelectView from '@/components/SelectView.vue'
import { formatFileSize } from '@/utils/utils'

const imageCountOptions = [
  {
    value: 30,
    label: '30张图/页',
  },
  {
    value: 40,
    label: '40张图/页',
  },
  {
    value: 50,
    label: '50张图/页',
  },
  {
    value: 100,
    label: '100张图/页',
  },
]

const folderList = ref<PicFolder[]>()
const loading = ref(true)
const images = ref<PicImages[]>([])
const total = ref(0)
const page = ref(1)
const perPage = ref(50)
const activeAlbum = ref('默认相册')
const showFolderPanel = ref(false)
const showImageInfo = ref(false)

// 显示图片信息
const picInfo = ref<PicImages>()
const picInfoDrawer = ref(false)
const handleShowPicInfo = (image: PicImages) => {
  picInfoDrawer.value = true
  picInfo.value = image
}

// 获取相册列表
const handleGetPicFolder = async () => {
  const res = await getPicFolderList()
  folderList.value = res.data.picFolderList
}

// 查询相册
const handleSetActiveAlbum = (folderName: string) => {
  activeAlbum.value = folderName
  handleGetPicList()
}

// 添加相册
const addPicFolderDialogVisible = ref(false)
const addFolderName = ref('')
const handleAddFolder = async () => {
  if (addFolderName.value) {
    const res = await addPicFolder(addFolderName.value)
    if (res.status === 200) {
      ElMessage.success(res.data.message)
      addFolderName.value = ''
      addPicFolderDialogVisible.value = false
      handleGetPicFolder()
    } else {
      ElMessage.error(res.data.message)
    }
  } else {
    ElMessage.error('请输入相册名称')
  }
}

// 编辑相册名称
const editPicFolderDialogVisible = ref(false)
const editFolderName = ref('')
const editFolderAttr = ref({
  folderId: 0,
  folderName: '',
})
const handleEditFolderAttr = (folderId: number, folderName: string) => {
  editPicFolderDialogVisible.value = true
  editFolderName.value = folderName
  editFolderAttr.value.folderId = folderId
  editFolderAttr.value.folderName = folderName
}
const handleEditFolder = async () => {
  if (editFolderName.value) {
    const res = await editPicFolder(
      editFolderName.value,
      editFolderAttr.value.folderId,
      editFolderAttr.value.folderName,
    )
    if (res.status === 200) {
      ElMessage.success(res.data.message)
      editPicFolderDialogVisible.value = false
      handleGetPicFolder()

      if (activeAlbum.value === editFolderAttr.value.folderName) {
        activeAlbum.value = editFolderName.value
      }
    } else {
      ElMessage.error(res.data.message)
    }
  } else {
    ElMessage.error('请输入相册名称')
  }
}

// 删除相册
const handleDeleteFolder = async (folderId: number, folderName: string) => {
  ElMessageBox.confirm(
    `你确定要删除 ${folderName} 吗？这将导致该文件下的所有图片被删除，并且无法恢复！`,
    {
      cancelButtonText: '取消',
      confirmButtonText: '确定',
      confirmButtonClass: 'el-button--danger',
      autofocus: false,
    },
  )
    .then(async () => {
      const res = await deletePicFolder(folderId, folderName)
      if (res.status === 200) {
        ElMessage.success(res.data.message)
        editFolderName.value = ''
        editPicFolderDialogVisible.value = false
        handleGetPicFolder()

        if (activeAlbum.value === folderName) {
          activeAlbum.value = '默认相册'
          handleGetPicList()
        }
      } else {
        ElMessage.error(res.data.message)
      }
    })
    .catch(() => {
      console.log('取消操作')
    })
}

// 获取图片列表
const handleGetPicList = async () => {
  loading.value = true
  const res = await getPicList({
    page: page.value,
    perPage: perPage.value,
    album: activeAlbum.value,
  })

  images.value = res.data.images
  total.value = res.data.total
  loading.value = false

  // 给 images.value 下的 元素添加 selected 属性
  images.value.forEach((item: PicImages) => {
    item.selected = false
  })
}

// 分页
const handleCurrentChange = (val: number) => {
  page.value = val
  handleGetPicList()
}

// 显示相册列表
const picListDialogVisible = ref(false)
const movePicList = ref()
const handleShowPicList = (picList: number[]) => {
  picListDialogVisible.value = true
  movePicList.value = picList
}

// 移动图片
const handleMovePic = async (pidList: number[], picPath: string) => {
  const res = await movePicService(pidList, picPath)
  if (res.status === 200) {
    ElMessage.success(res.data.message)
    handleGetPicList()
    handleGetPicFolder()
  } else {
    ElMessage.error(res.data.message)
  }

  picListDialogVisible.value = false
}

// 选择图片
const selectImage = (isOverlap: boolean, index: number) => {
  if (isOverlap) {
    images.value[index].selected = true
  } else {
    images.value[index].selected = false
  }
}

// 初始化
onMounted(async () => {
  handleGetPicFolder()
  handleGetPicList()
})
</script>

<template>
  <div id="pic" v-loading="loading">
    <el-container>
      <el-aside class="aside" :class="{ close: !showFolderPanel }">
        <el-menu class="menu" default-active="0">
          <el-menu-item
            v-for="(item, index) in folderList"
            :key="index + 1"
            :index="index + 1"
            @click="handleSetActiveAlbum(item.picFolderName)"
          >
            <el-icon><Folder /></el-icon>
            <span>{{ item.picFolderName }} ({{ item.picCount }})</span>
            <el-dropdown
              placement="bottom-start"
              class="more"
              v-if="item.picFolderName != '默认相册'"
            >
              <el-icon><More /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleEditFolderAttr(item.pid, item.picFolderName)"
                    ><el-icon><Edit /></el-icon>编辑名称</el-dropdown-item
                  >
                  <el-dropdown-item
                    class="delete"
                    @click="handleDeleteFolder(item.pid, item.picFolderName)"
                    ><el-icon><Delete /></el-icon>删除相册</el-dropdown-item
                  >
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-menu-item>
          <el-menu-item @click="addPicFolderDialogVisible = true">
            <el-icon><Plus /></el-icon>
            <span>新建相册</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="main">
        <el-header class="options">
          <div class="options-left">
            <div class="show-folder-panel">
              <el-button type="primary" @click="showFolderPanel = !showFolderPanel"
                >{{ showFolderPanel ? '收起' : '展开' }}相册</el-button
              >
            </div>
            <div class="show-image-info">
              <el-switch v-model="showImageInfo" />
              <span>显示图片信息</span>
            </div>
          </div>
          <div class="options-mid">
            <p>{{ activeAlbum }}</p>
          </div>
          <div class="options-right">
            <div class="show-image-count">
              <el-select
                v-model="perPage"
                placeholder="图片/页"
                style="width: 240px"
                @change="handleGetPicList"
              >
                <el-option
                  v-for="item in imageCountOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </div>
          </div>
        </el-header>
        <el-main style="padding: 0">
          <div class="empty-info" v-if="!images.length">
            <p>什么都没有~</p>
          </div>
          <el-scrollbar view-style="height: calc(100vh - 108px)" v-else>
            <SelectView
              v-viewer
              :showImageInfo="showImageInfo"
              :images="images"
              :selectImage="selectImage"
            >
            </SelectView>
            <div class="pagination-box">
              <el-pagination
                background
                layout="prev, pager, next"
                :total="total"
                :page-size="perPage"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-scrollbar>

          <el-drawer
            class="pic-drawer"
            v-model="picInfoDrawer"
            :title="picInfo?.picName"
            size="20%"
          >
            <div class="drawer-item">
              <p class="title">相册名称</p>
              <p class="text">{{ picInfo?.picPath }}</p>
            </div>
            <div class="drawer-item">
              <p class="title">图片名称</p>
              <p class="text">{{ picInfo?.picName }}</p>
            </div>
            <div class="drawer-item">
              <p class="title">图片原始名称</p>
              <p class="text">{{ picInfo?.picOriginalName }}</p>
            </div>
            <div class="drawer-item">
              <p class="title">图片大小</p>
              <p class="text">{{ formatFileSize(picInfo?.picFileSize || 0) }}</p>
            </div>
            <div class="drawer-item">
              <p class="title">图片类型</p>
              <p class="text">{{ picInfo?.picType }}</p>
            </div>
            <div class="drawer-item">
              <p class="title">尺寸</p>
              <p class="text">{{ picInfo?.picSize }}</p>
            </div>
            <div class="drawer-item">
              <p class="title">上传时间</p>
              <p class="text">{{ picInfo?.uploadTime }}</p>
            </div>
          </el-drawer>
        </el-main>
      </el-main>
    </el-container>

    <el-dialog v-model="addPicFolderDialogVisible" title="添加相册" width="500">
      <el-input v-model="addFolderName" placeholder="请输入相册名称"></el-input>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleAddFolder"> 添加 </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="editPicFolderDialogVisible" title="编辑相册" width="500">
      <el-input v-model="editFolderName" placeholder="请输入相册名称"></el-input>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleEditFolder"> 编辑 </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="picListDialogVisible" title="选择要移动到的相册" width="500">
      <div
        v-for="(item, index) in folderList"
        :key="index + 1"
        :index="index + 1"
        @click="handleMovePic(movePicList, item.picFolderName)"
        class="folder-item"
      >
        <el-icon><Folder /></el-icon>
        <span>{{ item.picFolderName }}</span>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="picListDialogVisible = false">取消</el-button>
        </div>
      </template>
    </el-dialog>
    <ContextMenu
      :handleGetPicList="handleGetPicList"
      :handleShowPicInfo="handleShowPicInfo"
      :handleShowPicList="handleShowPicList"
      :handleMovePic="handleMovePic"
      :handleGetPicFolder="handleGetPicFolder"
    />
  </div>
</template>

<style lang="scss" scoped>
@use '@/assets/scss/pic/index.scss';
</style>
