<script setup lang="ts">
import { ref, reactive } from 'vue'

interface Block {
  id: number
  selected: boolean
  url: string
}

const blocks = reactive<Block[]>(
  Array.from({ length: 100 }, (_, i) => ({
    id: i,
    selected: false,
    url: 'http://pic.ksamar.top/i/2025/01/03/6776c2c1a75f3.jpg',
  })),
)

const blockListRef = ref<HTMLElement | null>(null)
const blockRefs = ref<HTMLElement[]>([])
const selectBoxRef = ref<HTMLElement | null>(null)

const isSelecting = ref(false)
const startCoords = reactive({ x: 0, y: 0 })
const currentCoords = reactive({ x: 0, y: 0 })

function startSelection(e: MouseEvent) {
  if (!blockListRef.value) return

  const rect = blockListRef.value.getBoundingClientRect()
  startCoords.x = e.clientX - rect.left
  startCoords.y = e.clientY - rect.top
  currentCoords.x = startCoords.x
  currentCoords.y = startCoords.y

  isSelecting.value = true
  if (selectBoxRef.value) {
    selectBoxRef.value.style.display = 'block'
    updateSelectBox()
  }
}

function handleMouseMove(e: MouseEvent) {
  if (!isSelecting.value || !blockListRef.value) return

  const rect = blockListRef.value.getBoundingClientRect()
  currentCoords.x = e.clientX - rect.left
  currentCoords.y = e.clientY - rect.top

  updateSelectBox()
  checkSelection()
}

function endSelection() {
  isSelecting.value = false
  if (selectBoxRef.value) {
    selectBoxRef.value.style.display = 'none'
  }
}

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

function checkSelection() {
  if (!blockListRef.value) return

  const containerRect = blockListRef.value.getBoundingClientRect()
  const selectRect = {
    left: Math.min(startCoords.x, currentCoords.x),
    top: Math.min(startCoords.y, currentCoords.y),
    right: Math.max(startCoords.x, currentCoords.x),
    bottom: Math.max(startCoords.y, currentCoords.y),
  }

  blockRefs.value.forEach((el, index) => {
    if (!el) return
    const blockRect = el.getBoundingClientRect()

    const relativeLeft = blockRect.left - containerRect.left
    const relativeTop = blockRect.top - containerRect.top
    const relativeRight = relativeLeft + blockRect.width
    const relativeBottom = relativeTop + blockRect.height

    const isOverlap = !(
      selectRect.right < relativeLeft ||
      selectRect.left > relativeRight ||
      selectRect.bottom < relativeTop ||
      selectRect.top > relativeBottom
    )

    if (isOverlap) {
      blocks[index].selected = true
    } else {
      blocks[index].selected = false
    }
  })
}

function deleteSelected() {
  // 从后往前删除避免索引变化
  blocks
    .map((b, i) => (b.selected ? i : -1))
    .filter((i) => i !== -1)
    .sort((a, b) => b - a)
    .forEach((i) => blocks.splice(i, 1))
}
</script>

<template>
  <div id="dashboard">
    <button @click="deleteSelected" class="delete-btn">删除选中</button>
    <div
      draggable="false"
      ref="blockListRef"
      class="block-list"
      @mousedown="startSelection"
      @mousemove="handleMouseMove"
      @mouseup="endSelection"
      @mouseleave="endSelection"
    >
      <img
        draggable="false"
        class="block"
        v-for="(block, index) in blocks"
        :key="block.id"
        :class="{ selected: block.selected }"
        :ref="
          (el) => {
            if (el) blockRefs[index] = el as HTMLElement
          }
        "
        :src="block.url"
      />
      <div ref="selectBoxRef" class="select-box"></div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.delete-btn {
  margin-bottom: 20px;
  padding: 8px 16px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;

  &:hover {
    background: #d32f2f;
  }
}

.block-list {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 8px;
  height: 700px;
}

.block {
  width: 100px;
  height: 100px;
  background: #ddd;
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  &.selected {
    background: #2196f3;
    box-shadow:
      0 0 0 2px white,
      0 0 0 4px #2196f3;
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
