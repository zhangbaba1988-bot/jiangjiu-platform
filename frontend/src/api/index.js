import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000
})

service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token') || localStorage.getItem('adminToken')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return res
  },
  error => {
    console.error('响应错误:', error)
    let message = '网络错误'
    if (error.response) {
      switch (error.response.status) {
        case 401:
          message = '未授权，请重新登录'
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址不存在'
          break
        case 500:
          message = '服务器错误'
          break
        default:
          message = error.response.data?.message || `请求错误 ${error.response.status}`
      }
    }
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export const knowledgeApi = {
  getList(params) {
    return service.get('/knowledge', { params })
  },
  getDetail(id) {
    return service.get(`/knowledge/${id}`)
  },
  getCategories() {
    return service.get('/knowledge/categories')
  }
}

export const productionApi = {
  getList(params) {
    return service.get('/production', { params })
  },
  getDetail(id) {
    return service.get(`/production/${id}`)
  },
  getStatistics() {
    return service.get('/production/statistics')
  }
}

export const wineryApi = {
  getList(params) {
    return service.get('/wineries', { params })
  },
  getDetail(id) {
    return service.get(`/wineries/${id}`)
  }
}

export const newsApi = {
  getList(params) {
    return service.get('/news', { params })
  },
  getDetail(id) {
    return service.get(`/news/${id}`)
  }
}

export const searchApi = {
  search(keyword) {
    return service.get('/search', { params: { keyword } })
  },
  getHotSearches() {
    return service.get('/search/hot')
  }
}

export const userApi = {
  getProfile() {
    return service.get('/user/profile')
  },
  updateProfile(data) {
    return service.put('/user/profile', data)
  },
  getFavorites() {
    return service.get('/user/favorites')
  },
  addFavorite(data) {
    return service.post('/user/favorites', data)
  },
  removeFavorite(id) {
    return service.delete(`/user/favorites/${id}`)
  },
  getHistory() {
    return service.get('/user/history')
  }
}

export const adminApi = {
  login(data) {
    return service.post('/admin/login', data)
  },
  getMembers() {
    return service.get('/admin/members')
  }
}

export default service
