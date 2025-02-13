<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { getSystemConfig, setSystemConfig } from '@/api/system'

interface SettingForm {
  name: string
}

const settingFormRef = ref<FormInstance>()
const settingForm = reactive<SettingForm>({
  name: '',
})

const settingFormRules = reactive<FormRules<SettingForm>>({
  name: [{ required: true, message: '请输入网站名称', trigger: 'blur' }],
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      const res = await setSystemConfig(settingForm)
      if (res.status === 200) {
        ElMessage.success(res.data.message)
        setTimeout(() => {
          window.location.reload()
        }, 500)
      } else {
        ElMessage.error(res.data.message)
      }
    }
  })
}

onMounted(async () => {
  const res = await getSystemConfig()
  settingForm.name = res.data.server.name
})
</script>
<template>
  <div id="setting">
    <el-row>
      <el-col :span="16" :offset="4">
        <el-card>
          <el-form
            ref="settingFormRef"
            :model="settingForm"
            :rules="settingFormRules"
            label-width="auto"
            class="setting-form"
          >
            <el-form-item label="网站名称" prop="name" class="web-name">
              <el-input v-model="settingForm.name" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="submitForm(settingFormRef)"> 保存更改 </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<style scoped lang="scss">
#setting {
  min-height: calc(100% - 32px);
  padding-top: 32px;
  background-color: #f3f4f6;
}
.web-name {
  flex-direction: column;
}
</style>
