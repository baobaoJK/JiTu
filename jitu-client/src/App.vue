<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { getSystemConfig } from './api/system'

onMounted(async () => {
  const res = await getSystemConfig()
  document.title = res.data.server.name
})
</script>

<template>
  <RouterView />
</template>

<style lang="scss">
@use './assets/scss/base.scss';
@use './assets/scss/element-plus.scss';
</style>
