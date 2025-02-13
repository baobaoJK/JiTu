<script setup lang="ts">
import { ElMessage, ElMessageBox } from 'element-plus'
import { ref, onMounted, onBeforeUnmount, nextTick, defineProps } from 'vue'
import { renamePic, deletePic } from '@/api/pic'
import type { PicImages } from '@/model/pic'

const props = defineProps<{
  handleGetPicList: () => void
  handleShowPicInfo: (image: PicImages) => void
  handleShowPicList: (pidList: number[]) => void
  handleMovePic: (pidList: number[], picPath: string) => void
  handleGetPicFolder: () => void
}>()

const visible = ref(false)
const position = ref({ x: 0, y: 0 })
const selectedImage = ref<PicImages | null>(null) // 存储选中的 image 数据
const images = ref<PicImages[] | null>(null) // 存储所有 image 数据
const menuRef = ref<HTMLDivElement | null>(null)
const targetElementClass = 'image-view' // 目标元素 class

const showMenu = (event: MouseEvent) => {
  event.preventDefault() // 阻止默认右键菜单

  //  取消在菜单上右键效果
  if (menuRef.value?.contains(event.target as Node)) return

  selectedImage.value = null

  // 初始菜单位置 = 鼠标位置
  let x = event.pageX
  let y = event.pageY

  visible.value = true // 先显示菜单

  // 等待 DOM 渲染后计算菜单大小
  nextTick(() => {
    if (!menuRef.value) return

    const menuWidth = menuRef.value.offsetWidth
    const menuHeight = menuRef.value.offsetHeight
    const windowWidth = window.innerWidth
    const windowHeight = window.innerHeight

    // **调整 X 方向（防止超出右侧）**
    if (x + menuWidth > windowWidth) {
      x = event.pageX - menuWidth
    }

    // **调整 Y 方向（防止超出底部）**
    if (y + menuHeight > windowHeight) {
      y = event.pageY - menuHeight
    }

    // 更新菜单位置
    position.value = { x, y }
  })

  const target = (event.target as HTMLElement).closest(`.${targetElementClass}`)
  if (!target) return // 不是目标元素，返回

  // 获取 Vue 绑定的 image 数据（从 DOM 解析 dataset）
  selectedImage.value = JSON.parse(target.getAttribute('data-image') || '{}')
  images.value = JSON.parse(target.getAttribute('data-select-images') || '{}')
}

const hideMenu = (event: MouseEvent) => {
  if (!menuRef.value?.contains(event.target as Node)) {
    visible.value = false
  }
}

const handleAction = async (action: string) => {
  switch (action) {
    case 'refresh':
      window.location.reload()
      break
    case 'copy':
      // 执行复制图片操作
      await copyImageToClipboard(selectedImage.value?.url || '')
      break
    case 'newWindow':
      // 执行新窗口打开操作
      newWindow(selectedImage.value?.url || '')
      break
    case 'moveToAlbum':
      // 执行移动到相册操作
      movePic('custom')
      break
    case 'removeFromAlbum':
      // 执行移出当前相册操作
      movePic('default')
      break
    case 'details':
      // 执行详细信息操作
      showPicInfo()
      break
    case 'rename':
      // 执行重命名操作
      await renameImage()
      break
    case 'delete':
      // 执行删除操作
      await deleteImage()
      break
    default:
      break
  }
  visible.value = false
}

// 复制图片
const copyImageToClipboard = async (imageUrl: string) => {
  try {
    const img = new Image()
    img.crossOrigin = 'anonymous' // 处理跨域问题
    img.src = imageUrl

    await new Promise((resolve, reject) => {
      img.onload = resolve
      img.onerror = reject
    })

    // 创建 Canvas
    const canvas = document.createElement('canvas')
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')
    if (!ctx) throw new Error('无法获取 Canvas 上下文')

    // 在 Canvas 上绘制图片
    ctx.drawImage(img, 0, 0, img.width, img.height)

    // 转换为 Blob
    canvas.toBlob(async (blob) => {
      if (!blob) throw new Error('图片转换失败')
      try {
        const clipboardItem = new ClipboardItem({ 'image/png': blob })
        await navigator.clipboard.write([clipboardItem])
        ElMessage.success('图片已复制到剪贴板！')
      } catch (err: unknown) {
        ElMessage.error('复制失败')
        console.log(err)
      }
    }, 'image/png') // 统一转为 PNG 格式
  } catch (error) {
    console.error('复制图片失败:', error)
  }
}

// 新窗口打开
const newWindow = (url: string) => {
  window.open(url, '_blank')
}

// 移动到相册
const movePic = async (moveType: string) => {
  const movePicList = []
  if (images.value?.length === 0) {
    movePicList.push(selectedImage.value?.pid || 0)
  } else {
    const picList = images.value?.map((item) => item.pid)
    if (picList) {
      movePicList.push(...picList)
    }
  }

  if (moveType === 'custom') {
    props.handleShowPicList(movePicList)
  } else {
    props.handleMovePic(movePicList, '默认相册')
  }
}

// 详细信息
const showPicInfo = () => {
  if (selectedImage.value) {
    props.handleShowPicInfo(selectedImage.value)
  }
}

// 重命名
const renameImage = async () => {
  ElMessageBox.prompt('请输入新的图片名称', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputPattern: /^[\u4e00-\u9fa5a-zA-Z0-9_ ]+$/,
    inputErrorMessage: '图片名称只能包含中文、英文、数字、空格和下划线',
    inputValue: selectedImage.value?.picName || '',
  })
    .then(async ({ value }) => {
      const res = await renamePic(selectedImage.value?.pid || 0, value)
      if (res.status === 200) {
        ElMessage.success(res.data.message)
        // window.location.reload()
        props.handleGetPicList()
      } else {
        ElMessage.error(res.data.message)
      }
    })
    .catch(() => {
      // ElMessage.info('已取消重命名')
    })
}

// 删除图片
const deleteImage = async () => {
  ElMessageBox.confirm('确定要删除该图片吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    confirmButtonClass: 'el-button--danger',
  })
    .then(async () => {
      const deletePicList: number[] = []

      if (images.value?.length === 0) {
        deletePicList.push(selectedImage.value?.pid || 0)
      } else {
        const picList = images.value?.map((item) => item.pid)
        if (picList) {
          deletePicList.push(...picList)
        }
      }

      const res = await deletePic(deletePicList)
      if (res.status === 200) {
        ElMessage.success(res.data.message)
        // window.location.reload()
        props.handleGetPicList()
        props.handleGetPicFolder()
      } else {
        ElMessage.error(res.data.message)
      }
    })
    .catch(() => {
      // ElMessage.info('已取消删除')
    })
}
// 初始化
onMounted(() => {
  document.addEventListener('contextmenu', showMenu)
  document.addEventListener('click', hideMenu)
})

onBeforeUnmount(() => {
  document.removeEventListener('contextmenu', showMenu)
  document.removeEventListener('click', hideMenu)
})
</script>

<template>
  <div
    v-show="visible"
    ref="menuRef"
    class="context-menu"
    :style="{ top: `${position.y}px`, left: `${position.x}px` }"
  >
    <ul v-if="selectedImage">
      <span>图片操作</span>
      <li @click="handleAction('refresh')">刷新</li>
      <li v-show="!selectedImage.selected" @click="handleAction('copy')">复制图片</li>
      <li v-show="!selectedImage.selected" @click="handleAction('newWindow')">新窗口打开</li>
      <li @click="handleAction('moveToAlbum')">移动到相册</li>
      <li v-show="selectedImage.picPath != '默认相册'" @click="handleAction('removeFromAlbum')">
        移出当前相册
      </li>
      <li v-show="!selectedImage.selected" @click="handleAction('details')">详细信息</li>
      <div style="border-top: #f0f0f0 1px solid; margin: 8px 0px"></div>
      <li v-show="!selectedImage.selected" @click="handleAction('rename')">重命名</li>
      <li @click="handleAction('delete')">删除</li>
    </ul>

    <ul v-else>
      <li @click="handleAction('refresh')">刷新</li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.context-menu {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  border-radius: 5px;
  overflow: hidden;
  min-width: 120px;

  ul {
    list-style: none;
    padding: 5px 0;
    margin: 0;
  }

  li {
    padding: 8px 15px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;

    &:hover {
      background: #f0f0f0;
    }
  }

  span {
    padding: 8px 15px;
    font-size: 12px;
    color: #999;
  }
}
</style>
