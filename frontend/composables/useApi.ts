import axios from 'axios'

export const useApi = () => {
  const config = useRuntimeConfig()
  const api = axios.create({ baseURL: config.public.apiBase })

  return {
    listFiles: (params: any = {}) => api.get('/files', { params }).then(r => r.data),
    uploadFile: (file: File, folder_id?: number) => {
      const fd = new FormData()
      fd.append('f', file)
      if (folder_id) fd.append('folder_id', String(folder_id))
      return api.post('/files/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } }).then(r => r.data)
    },
    fileDetail: (id: number) => api.get(`/files/${id}`).then(r => r.data),
    download: (id: number) => window.location.href = `${config.public.apiBase}/files/${id}/download`,
    deleteFile: (id: number) => api.delete(`/files/${id}`).then(r => r.data),
    listFolders: () => api.get('/folders').then(r => r.data),
    createFolder: (name: string, parent_id?: number) => api.post('/folders', { name, parent_id }).then(r => r.data),
    updateMetadata: (id: number, payload: { json: any, tags: string }) => api.patch(`/metadata/${id}`, payload).then(r => r.data),
    recluster: () => api.post('/analytics/recluster').then(r => r.data),
    getClusters: () => api.get('/analytics/clusters').then(r => r.data)
  }
}
