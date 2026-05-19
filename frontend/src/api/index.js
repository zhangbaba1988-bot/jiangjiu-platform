import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 添加token
    const token = localStorage.getItem('token')
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

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    // 这里可以根据后端的响应码做统一处理
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

// 知识库API
export const knowledgeApi = {
  // 获取文章列表
  getList(params) {
    return service.get('/knowledge', { params })
  },
  // 获取文章详情
  getDetail(id) {
    return service.get(`/knowledge/${id}`)
  },
  // 获取文章分类
  getCategories() {
    return service.get('/knowledge/categories')
  }
}

// 产区数据API
export const productionApi = {
  // 获取产区列表
  getList(params) {
    return service.get('/production', { params })
  },
  // 获取产区详情
  getDetail(id) {
    return service.get(`/production/${id}`)
  },
  // 获取统计数据
  getStatistics() {
    return service.get('/production/statistics')
  }
}

// 酒厂名录API
export const wineryApi = {
  // 获取酒厂列表
  getList(params) {
    return service.get('/wineries', { params })
  },
  // 获取酒厂详情
  getDetail(id) {
    return service.get(`/wineries/${id}`)
  }
}

// 资讯API
export const newsApi = {
  // 获取资讯列表
  getList(params) {
    return service.get('/news', { params })
  },
  // 获取资讯详情
  getDetail(id) {
    return service.get(`/news/${id}`)
  }
}

// 搜索API
export const searchApi = {
  // 全站搜索
  search(keyword) {
    return service.get('/search', { params: { keyword } })
  },
  // 获取热门搜索
  getHotSearches() {
    return service.get('/search/hot')
  }
}

// 用户API
export const userApi = {
  // 获取用户信息
  getProfile() {
    return service.get('/user/profile')
  },
  // 获取收藏列表
  getFavorites() {
    return service.get('/user/favorites')
  },
  // 添加收藏
  addFavorite(data) {
    return service.post('/user/favorites', data)
  },
  // 取消收藏
  removeFavorite(id) {
    return service.delete(`/user/favorites/${id}`)
  },
  // 获取浏览历史
  getHistory() {
    return service.get('/user/history')
  }
}

export default service
