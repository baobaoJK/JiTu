import axios from 'axios'
// import router from '@/router'
import { ElMessage } from 'element-plus'

export const baseURL = 'https://127.0.0.1:4932/api'
const request = axios.create({
  baseURL: baseURL,
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    // 失败执行promise
    return Promise.reject(error)
  },
)
// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 判断返回的数据
    const { status } = response.data
    if (status) {
      return response.data
    } else {
      ElMessage({ type: 'error', message: response.data.message })
      return Promise.reject(response)
    }
  },
  async (error) => {
    // error.message
    ElMessage.error(error.response.data.message)
    return Promise.reject(error)
  },
)

export default request
