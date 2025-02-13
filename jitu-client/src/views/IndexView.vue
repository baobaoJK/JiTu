<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getSystemConfig } from '@/api/system'
const router = useRouter()

const handleClick = () => {
  router.push('/layout')
}

const name = ref('')
onMounted(async () => {
  const res = await getSystemConfig()
  name.value = res.data.server.name
})
</script>
<template>
  <div id="index" @click="handleClick">
    <img class="background" src="/background.jpg" alt="background.jpg" />
    <p class="float-text">点击任意位置进入{{ name }}</p>
  </div>
</template>
<style scoped lang="scss">
@use '@/assets/scss/variable.scss' as *;

@keyframes float {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
  100% {
    opacity: 1;
  }
}
#index {
  @extend %fullview;
  overflow: hidden;
}

.background {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.float-text {
  position: absolute;
  bottom: 80px;
  margin-left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 24px;
  letter-spacing: 16px;
  animation: float 2s infinite;
}
</style>
