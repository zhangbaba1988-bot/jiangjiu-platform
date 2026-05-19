import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const userInfo = ref(null)
  const favorites = ref([])
  const searchHistory = ref([])
  const token = ref(localStorage.getItem('token') || '')

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)

  // 方法
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  const fetchUserInfo = async () => {
    if (!isLoggedIn.value) return
    try {
      const res = await userApi.getProfile()
      userInfo.value = res.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  const fetchFavorites = async () => {
    if (!isLoggedIn.value) return
    try {
      const res = await userApi.getFavorites()
      favorites.value = res.data
    } catch (error) {
      console.error('获取收藏列表失败:', error)
    }
  }

  const addFavorite = async (item) => {
    if (!isLoggedIn.value) return false
    try {
      await userApi.addFavorite(item)
      favorites.value.unshift(item)
      return true
    } catch (error) {
      console.error('添加收藏失败:', error)
      return false
    }
  }

  const removeFavorite = async (id) => {
    if (!isLoggedIn.value) return false
    try {
      await userApi.removeFavorite(id)
      favorites.value = favorites.value.filter(item => item.id !== id)
      return true
    } catch (error) {
      console.error('取消收藏失败:', error)
      return false
    }
  }

  const addSearchHistory = (keyword) => {
    if (!searchHistory.value.includes(keyword)) {
      searchHistory.value.unshift(keyword)
      if (searchHistory.value.length > 10) {
        searchHistory.value.pop()
      }
      localStorage.setItem('searchHistory', JSON.stringify(searchHistory.value))
    }
  }

  const clearSearchHistory = () => {
    searchHistory.value = []
    localStorage.removeItem('searchHistory')
  }

  // 初始化搜索历史
  const initSearchHistory = () => {
    const saved = localStorage.getItem('searchHistory')
    if (saved) {
      searchHistory.value = JSON.parse(saved)
    }
  }

  return {
    // 状态
    userInfo,
    favorites,
    searchHistory,
    token,
    // 计算属性
    isLoggedIn,
    // 方法
    setToken,
    logout,
    fetchUserInfo,
    fetchFavorites,
    addFavorite,
    removeFavorite,
    addSearchHistory,
    clearSearchHistory,
    initSearchHistory
  }
})
