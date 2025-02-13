import type { AxiosResponse } from 'axios'
import request from './request'

// 获取图片数量
export const getPicCount = () => {
  return request.get('/getPicCount').then((res: AxiosResponse) => {
    return res
  })
}

// 获取图片列表
export const getPicList = (params: unknown) => {
  return request.get('/getPicList', { params }).then((res: AxiosResponse) => {
    return res
  })
}

// 添加相册
export const addPicFolder = (folderName: string) => {
  return request.post('/picFolder', { folderName }).then((res: AxiosResponse) => {
    return res
  })
}

// 获取相册列表
export const getPicFolderList = () => {
  return request.get('/picFolder').then((res: AxiosResponse) => {
    return res
  })
}

// 编辑相册名称
export const editPicFolder = (rename: string, folderId: number, folderName: string) => {
  return request.put('/picFolder', { rename, folderId, folderName }).then((res: AxiosResponse) => {
    return res
  })
}

// 删除相册
export const deletePicFolder = (folderId: number, folderName: string) => {
  return request
    .delete('/picFolder', { data: { folderId, folderName } })
    .then((res: AxiosResponse) => {
      return res
    })
}

// 移动图片
export const movePicService = (pidList: number[], picPath: string) => {
  return request.post('/pic', { pidList, picPath }).then((res: AxiosResponse) => {
    return res
  })
}

// 重命名
export const renamePic = (pid: number, rename: string) => {
  return request.put('/pic', { pid, rename }).then((res: AxiosResponse) => {
    return res
  })
}

// 删除图片
export const deletePic = (deletePicList: number[]) => {
  return request.delete('/pic', { data: { deletePicList } }).then((res: AxiosResponse) => {
    return res
  })
}
