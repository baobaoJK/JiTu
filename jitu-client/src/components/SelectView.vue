<script setup lang="ts">
import { ref, reactive, defineProps } from 'vue'
import type { PicImages } from '@/model/pic'

const props = defineProps<{
  images: PicImages[]
  showImageInfo: boolean
  selectImage: (isOverlap: boolean, index: number) => void
}>()
/**
 * 框选图片
 */
const imagesRef = ref<HTMLElement>()
const galleryRefs = ref<HTMLElement[]>([])
const galleryListRef = ref<HTMLElement | null>(null)
const selectBoxRef = ref<HTMLElement | null>(null)

const isSelecting = ref(false)
const startCoords = reactive({ x: 0, y: 0 })
const currentCoords = reactive({ x: 0, y: 0 })

// 开始选择
function startSelection(e: MouseEvent) {
  // e.preventDefault()
  if (e.button === 0) {
    props.images.forEach((item: PicImages) => {
      item.selected = false
    })

    // 判断点击的是否 galleryRefs
    const target = e.target as HTMLElement
    const isGallery = galleryRefs.value.some((item) => item.contains(target))
    if (isGallery) {
      isSelecting.value = false
      return
    }
  }
  if (e.button === 2) return
  if (!galleryListRef.value) return

  const rect = galleryListRef.value.getBoundingClientRect()
  const scrollElement = document.querySelector('.el-scrollbar__wrap') // 获取 el-scrollbar 的滚动元素
  const scrollLeft = scrollElement?.scrollLeft || 0
  const scrollTop = scrollElement?.scrollTop || 0
  startCoords.x = e.clientX - rect.left - scrollLeft
  startCoords.y = e.clientY - rect.top - scrollTop
  currentCoords.x = startCoords.x
  currentCoords.y = startCoords.y

  isSelecting.value = true
  if (selectBoxRef.value) {
    selectBoxRef.value.style.display = 'block'
    updateSelectBox()
  }
}

// 检测鼠标移动
function handleMouseMove(e: MouseEvent) {
  if (!isSelecting.value || !galleryListRef.value) return

  const rect = galleryListRef.value.getBoundingClientRect()
  const scrollElement = document.querySelector('.el-scrollbar__wrap') // 获取 el-scrollbar 的滚动元素
  const scrollLeft = scrollElement?.scrollLeft || 0
  const scrollTop = scrollElement?.scrollTop || 0
  currentCoords.x = e.clientX - rect.left - scrollLeft
  currentCoords.y = e.clientY - rect.top - scrollTop

  updateSelectBox()
  checkSelection()
}

// 结束选择
function endSelection() {
  isSelecting.value = false
  if (selectBoxRef.value) {
    selectBoxRef.value.style.display = 'none'
  }
}

// 更新框选盒子
function updateSelectBox() {
  if (!selectBoxRef.value) return

  const left = Math.min(startCoords.x, currentCoords.x)
  const top = Math.min(startCoords.y, currentCoords.y)
  const width = Math.abs(currentCoords.x - startCoords.x)
  const height = Math.abs(currentCoords.y - startCoords.y)

  selectBoxRef.value.style.left = `${left}px`
  selectBoxRef.value.style.top = `${top}px`
  selectBoxRef.value.style.width = `${width}px`
  selectBoxRef.value.style.height = `${height}px`
}

// 选择图片
function checkSelection() {
  if (!galleryListRef.value) return

  const containerRect = galleryListRef.value.getBoundingClientRect()
  const scrollElement = document.querySelector('.el-scrollbar__wrap') // 获取 el-scrollbar 的滚动元素
  const scrollLeft = scrollElement?.scrollLeft || 0
  const scrollTop = scrollElement?.scrollTop || 0
  const selectRect = {
    left: Math.min(startCoords.x, currentCoords.x),
    top: Math.min(startCoords.y, currentCoords.y),
    right: Math.max(startCoords.x, currentCoords.x),
    bottom: Math.max(startCoords.y, currentCoords.y),
  }

  galleryRefs.value.forEach((el, index) => {
    if (!el) return
    const blockRect = el.getBoundingClientRect()

    const relativeLeft = blockRect.left - containerRect.left - scrollLeft
    const relativeTop = blockRect.top - containerRect.top - scrollTop
    const relativeRight = relativeLeft + blockRect.width
    const relativeBottom = relativeTop + blockRect.height

    const isOverlap = !(
      selectRect.right < relativeLeft ||
      selectRect.left > relativeRight ||
      selectRect.bottom < relativeTop ||
      selectRect.top > relativeBottom
    )

    props.selectImage(isOverlap, index)
    //   设置 props.images 属性
  })
}
</script>
<template>
  <div
    id="select"
    class="gallery"
    ref="galleryListRef"
    @mousedown="startSelection"
    @mousemove="handleMouseMove"
    @mouseup="endSelection"
    @mouseleave="endSelection"
  >
    <div
      class="image-view"
      v-for="(image, index) in images"
      :key="image.pid"
      :data-image="JSON.stringify(image)"
      :data-select-images="JSON.stringify(images.filter((img) => img.selected))"
      :class="{ selected: image.selected }"
      :ref="
        (el) => {
          if (el) galleryRefs[index] = el as HTMLElement
        }
      "
    >
      <img :src="image.url" ref="imagesRef" />
      <div class="image-info" v-if="props.showImageInfo">
        <span>{{ image.picName }}</span>
        <p>{{ image.uploadTime }}</p>
      </div>
    </div>
    <div ref="selectBoxRef" class="select-box"></div>
  </div>
</template>
<style scoped lang="scss">
@use '@/assets/scss/variable.scss' as *;
.gallery {
  columns: 10;
  column-gap: 10px;
  padding: 10px;
  min-height: calc(100% - 128px);

  .image-view {
    position: relative;
    display: flex;
    width: 100%;
    height: auto;
    margin-bottom: 10px;
    border-radius: 8px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    border: 3px solid transparent;
    box-sizing: border-box;
    overflow: hidden;

    &:hover {
      border: 3px solid $mainColor;
    }

    &.selected {
      border: 3px solid $subColor;
    }
    img {
      width: 100%;
      height: 100%;
    }

    .image-info {
      position: absolute;
      width: 100%;
      padding: 6px;
      bottom: 0px;
      font-size: 12px;
      color: white;
      box-sizing: border-box;
      background: linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 1));
    }
  }
}
.select-box {
  position: absolute;
  display: none;
  background: rgba(33, 150, 243, 0.1);
  border: 2px dashed #2196f3;
  pointer-events: none;
  border-radius: 4px;
}
</style>
