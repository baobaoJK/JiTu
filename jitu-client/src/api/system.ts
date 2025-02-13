import type { AxiosResponse } from 'axios'
import request from './request'

// 获取系统配置信息
export const getSystemConfig = () => {
  return request.get('/getConfig').then((res: AxiosResponse) => {
    return res
  })
}

// 设置系统配置信息
export const setSystemConfig = (data: { name: string }) => {
  return request
    .put('/setConfig', {
      name: data.name,
    })
    .then((res: AxiosResponse) => {
      return res
    })
}
