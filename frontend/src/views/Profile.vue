<template>
  <div class="profile-page">
    <div class="page-header">
      <div>
        <p class="eyebrow">个人中心</p>
        <h1>管理你的酱酒学习轨迹</h1>
        <p class="subtitle">查看收藏、回顾浏览历史，并集中管理你在论坛发表的内容。</p>
      </div>
      <div class="page-actions">
        <button class="ghost-btn" @click="showEdit = true">✏️ 修改资料</button>
        <button class="ghost-btn" @click="logout">🚪 退出登录</button>
        <button class="refresh-btn" @click="loadProfileData">🔄 刷新数据</button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="loading-icon">⏳</div>
      <p>加载中，请稍后...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button class="refresh-btn" @click="loadProfileData">重新尝试</button>
    </div>

    <template v-else>
      <section class="user-card">
        <div v-if="isAvatarUrl(profile.avatar)" class="avatar-wrap">
          <img class="avatar" :src="profile.avatar" :alt="profile.nickname || '用户头像'" />
        </div>
        <div v-else class="avatar-badge" :style="{ background: getAvatarGradient(profile.avatar) }">
          <span>{{ getAvatarIcon(profile.avatar) }}</span>
        </div>
        <div class="user-info">
          <div>
            <p class="user-label">当前用户</p>
            <h2>{{ profile.nickname || '酱酒爱好者' }}</h2>
          </div>
          <p class="user-id">ID：{{ profile.id || '--' }}</p>
          <div class="user-tags">
            <button
              type="button"
              class="user-tag-btn"
              :class="{ active: activeTab === 'favorites' }"
              @click="activeTab = 'favorites'"
            >
              ⭐ 收藏 {{ favoriteCount }}
            </button>
            <button
              type="button"
              class="user-tag-btn"
              :class="{ active: activeTab === 'history' }"
              @click="activeTab = 'history'"
            >
              📋 历史 {{ historyCount }}
            </button>
            <button
              type="button"
              class="user-tag-btn"
              :class="{ active: activeTab === 'posts' }"
              @click="activeTab = 'posts'"
            >
              💬 发帖 {{ forumPosts.length }}
            </button>
          </div>
        </div>
      </section>

      <section class="content-panel panel">
        <div v-if="activeTab === 'favorites'">
          <div class="panel-header">
            <div>
              <p class="eyebrow">我的收藏</p>
              <h3>收藏的内容</h3>
            </div>
            <span class="panel-count">{{ favorites.length }} 条</span>
          </div>

          <div v-if="favorites.length" class="item-list">
            <div v-for="item in favorites" :key="item.id" class="item-card">
              <router-link :to="getDetailPath(item)" class="item-main">
                <p class="item-tag">{{ getItemTypeLabel(item) }}</p>
                <h4>{{ item.title || item.name || '未命名内容' }}</h4>
                <p class="item-summary">{{ getItemSummary(item) }}</p>
              </router-link>
              <button class="remove-btn" @click="removeFavorite(item.id)">取消收藏</button>
            </div>
          </div>

          <div v-else class="empty-state">
            <div class="empty-icon">⭐</div>
            <p>还没有收藏内容，先去浏览知识库、产区或资讯吧。</p>
            <div class="empty-actions">
              <router-link to="/knowledge" class="ghost-btn">去知识库</router-link>
              <router-link to="/news" class="ghost-btn">看行业资讯</router-link>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'history'">
          <div class="panel-header">
            <div>
              <p class="eyebrow">浏览历史</p>
              <h3>最近浏览过的内容</h3>
            </div>
            <span class="panel-count">{{ history.length }} 条</span>
          </div>

          <div v-if="history.length" class="item-list">
            <router-link
              v-for="item in history"
              :key="item.id"
              :to="getDetailPath(item)"
              class="item-card"
            >
              <div>
                <p class="item-tag">{{ getItemTypeLabel(item) }}</p>
                <h4>{{ item.title || item.name || '未命名内容' }}</h4>
                <p class="item-summary">{{ getItemSummary(item) }}</p>
              </div>
              <span class="item-arrow">→</span>
            </router-link>
          </div>

          <div v-else class="empty-state">
            <div class="empty-icon">📋</div>
            <p>浏览历史为空，先访问一些内容就会自动记录。</p>
            <div class="empty-actions">
              <router-link to="/wineries" class="ghost-btn">查看酒厂名录</router-link>
              <router-link to="/production" class="ghost-btn">查看产区数据</router-link>
            </div>
          </div>
        </div>

        <div v-else>
          <div class="panel-header">
            <div>
              <p class="eyebrow">论坛内容管理</p>
              <h3>我发表的内容</h3>
            </div>
            <div class="forum-actions">
              <router-link to="/forum" class="ghost-btn">去论坛发帖</router-link>
            </div>
          </div>

          <div v-if="forumPosts.length" class="item-list">
            <div v-for="post in forumPosts" :key="post.id" class="item-card forum-post-card">
              <div class="forum-post-main">
                <p class="item-tag">{{ post.category }}</p>
                <h4>{{ post.title }}</h4>
                <p class="item-summary">{{ post.content }}</p>
                <div class="post-meta">
                  <span>发布时间：{{ post.createdAt || '刚刚' }}</span>
                  <span>回复数：{{ post.replies || 0 }}</span>
                </div>
              </div>
              <button class="remove-btn" @click="deleteForumPost(post.id)">删除</button>
            </div>
          </div>

          <div v-else class="empty-state">
            <div class="empty-icon">💬</div>
            <p>还没有在论坛发表过内容，去论坛发一条讨论吧。</p>
            <div class="empty-actions">
              <router-link to="/forum" class="ghost-btn">前往论坛发帖</router-link>
            </div>
          </div>
        </div>
      </section>
    </template>

    <div v-if="showEdit" class="modal-mask" @click.self="showEdit = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>修改资料</h3>
          <button class="close-btn" @click="showEdit = false">✕</button>
        </div>
        <div class="modal-body">
          <label class="field-label">昵称</label>
          <input v-model="editForm.nickname" class="field-input" placeholder="请输入昵称" />

          <label class="field-label">头像风格</label>
          <div class="avatar-picker">
            <button
              v-for="option in avatarOptions"
              :key="option.key"
              type="button"
              class="avatar-option"
              :class="{ active: editForm.avatar === option.key }"
              @click="editForm.avatar = option.key"
            >
              <span class="avatar-option-swatch" :style="{ background: option.gradient }">{{ option.icon }}</span>
              <span>{{ option.label }}</span>
            </button>
          </div>

          <div class="avatar-preview">
            <div v-if="isAvatarUrl(editForm.avatar)" class="avatar-wrap">
              <img :src="editForm.avatar" :alt="editForm.nickname || '头像预览'" />
            </div>
            <div v-else class="avatar-badge preview-avatar" :style="{ background: getAvatarGradient(editForm.avatar) }">
              <span>{{ getAvatarIcon(editForm.avatar) }}</span>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="ghost-btn" @click="showEdit = false">取消</button>
          <button class="refresh-btn" @click="saveProfile">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { userApi } from '@/api'

const router = useRouter()
const defaultAvatarKey = 'amber'
const forumStorageKey = 'jiangjiu_forum_posts'

const avatarOptions = [
  { key: 'amber', label: '金黄', icon: '🍶', gradient: 'linear-gradient(135deg, #F4D27A 0%, #B27818 100%)' },
  { key: 'brown', label: '棕韵', icon: '🍂', gradient: 'linear-gradient(135deg, #A56A3B 0%, #5B2F18 100%)' },
  { key: 'green', label: '青翠', icon: '🌿', gradient: 'linear-gradient(135deg, #8CCB8C 0%, #2F6B4B 100%)' },
  { key: 'blue', label: '湖蓝', icon: '🌊', gradient: 'linear-gradient(135deg, #86C8E6 0%, #235E8B 100%)' }
]

const loading = ref(true)
const error = ref('')
const showEdit = ref(false)
const activeTab = ref('favorites')
const profile = ref({
  id: '--',
  nickname: '酱酒爱好者',
  avatar: defaultAvatarKey,
  favorite_count: 0,
  history_count: 0
})
const favorites = ref([])
const history = ref([])
const forumPosts = ref([])
const editForm = ref({
  nickname: '',
  avatar: defaultAvatarKey
})

const favoriteCount = computed(() => favorites.value.length)
const historyCount = computed(() => history.value.length)

const isAvatarUrl = (value) => typeof value === 'string' && /^https?:\/\//i.test(value)

const normalizeAvatarValue = (value) => {
  if (!value) return defaultAvatarKey
  return isAvatarUrl(value) ? defaultAvatarKey : value
}

const getAvatarOption = (value) => {
  const normalized = normalizeAvatarValue(value)
  return avatarOptions.find(option => option.key === normalized) || avatarOptions.find(option => option.key === defaultAvatarKey)
}

const getAvatarGradient = (value) => getAvatarOption(value)?.gradient || avatarOptions.find(option => option.key === defaultAvatarKey).gradient

const getAvatarIcon = (value) => getAvatarOption(value)?.icon || avatarOptions.find(option => option.key === defaultAvatarKey).icon

const normalizeList = (payload) => {
  if (!payload) return []
  if (Array.isArray(payload)) return payload
  if (Array.isArray(payload.list)) return payload.list
  return []
}

const applyLocalOverride = () => {
  const saved = localStorage.getItem('profile_override')
  if (!saved) return

  try {
    const override = JSON.parse(saved)
    profile.value = {
      ...profile.value,
      ...override,
      avatar: override.avatar || profile.value.avatar || defaultAvatarKey
    }
    editForm.value = {
      nickname: override.nickname || profile.value.nickname || '',
      avatar: override.avatar || profile.value.avatar || defaultAvatarKey
    }
  } catch (error) {
    console.error('读取本地资料失败:', error)
  }
}

const saveLocalOverride = (nextProfile) => {
  localStorage.setItem('profile_override', JSON.stringify(nextProfile))
}

const getItemTypeLabel = (item) => {
  if (item.type) {
    return item.type === 'company' ? '资讯' : item.type
  }

  if (item.category) return '知识库'
  if (item.region || item.area) return '产区'
  if (item.production || item.brand || item.established) return '酒厂'
  return '内容'
}

const getDetailPath = (item) => {
  if (item.type !== undefined || item.category !== undefined) {
    return item.type ? `/news/${item.id}` : `/knowledge/${item.id}`
  }

  if (item.region || item.area) return `/production/${item.id}`
  if (item.production || item.brand || item.established) return `/wineries/${item.id}`

  return '/knowledge'
}

const getItemSummary = (item) => {
  return item.summary || item.description || item.story || item.detail || '暂无简介'
}

const loadForumPosts = () => {
  const saved = localStorage.getItem(forumStorageKey)
  if (!saved) {
    forumPosts.value = []
    return
  }

  try {
    const parsed = JSON.parse(saved)
    forumPosts.value = Array.isArray(parsed) ? parsed : []
  } catch (error) {
    console.error('读取论坛发帖失败:', error)
    forumPosts.value = []
  }
}

const deleteForumPost = (id) => {
  forumPosts.value = forumPosts.value.filter(post => post.id !== id)
  localStorage.setItem(forumStorageKey, JSON.stringify(forumPosts.value))
  ElMessage.success('已删除该帖子')
}

const loadProfileData = async () => {
  loading.value = true
  error.value = ''

  try {
    const [profileRes, favoritesRes, historyRes] = await Promise.allSettled([
      userApi.getProfile(),
      userApi.getFavorites(),
      userApi.getHistory()
    ])

    if (profileRes.status === 'fulfilled' && profileRes.value?.data) {
      profile.value = {
        ...profile.value,
        ...profileRes.value.data,
        avatar: isAvatarUrl(profileRes.value.data.avatar) ? profileRes.value.data.avatar : (profileRes.value.data.avatar || defaultAvatarKey)
      }
    }

    applyLocalOverride()

    favorites.value = normalizeList(favoritesRes.status === 'fulfilled' ? favoritesRes.value?.data : null)
    history.value = normalizeList(historyRes.status === 'fulfilled' ? historyRes.value?.data : null)

    profile.value.favorite_count = favorites.value.length
    profile.value.history_count = history.value.length

    editForm.value = {
      nickname: profile.value.nickname || '',
      avatar: isAvatarUrl(profile.value.avatar) ? defaultAvatarKey : (profile.value.avatar || defaultAvatarKey)
    }

    loadForumPosts()
  } catch (e) {
    error.value = '用户数据加载失败，请稍后再试'
  } finally {
    loading.value = false
  }
}

const removeFavorite = async (id) => {
  try {
    await userApi.removeFavorite(id)
    favorites.value = favorites.value.filter(item => item.id !== id)
    profile.value.favorite_count = favorites.value.length
    ElMessage.success('已取消收藏')
  } catch (error) {
    console.error('取消收藏失败:', error)
  }
}

const saveProfile = async () => {
  try {
    const nextProfile = {
      ...profile.value,
      nickname: editForm.value.nickname || profile.value.nickname || '酱酒爱好者',
      avatar: editForm.value.avatar || defaultAvatarKey
    }

    const res = await userApi.updateProfile({
      nickname: nextProfile.nickname,
      avatar: nextProfile.avatar
    })

    profile.value = {
      ...profile.value,
      ...res.data,
      avatar: isAvatarUrl(res.data.avatar) ? res.data.avatar : (res.data.avatar || defaultAvatarKey)
    }

    saveLocalOverride(profile.value)
    editForm.value = {
      nickname: profile.value.nickname,
      avatar: isAvatarUrl(profile.value.avatar) ? defaultAvatarKey : (profile.value.avatar || defaultAvatarKey)
    }
    showEdit.value = false
    ElMessage.success('资料已更新')
  } catch (error) {
    console.error('更新资料失败:', error)
    ElMessage.error('资料更新失败')
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('adminToken')
  localStorage.removeItem('profile_override')
  profile.value = {
    id: '--',
    nickname: '酱酒爱好者',
    avatar: defaultAvatarKey,
    favorite_count: 0,
    history_count: 0
  }
  favorites.value = []
  history.value = []
  forumPosts.value = []
  loading.value = false
  error.value = ''
  ElMessage.success('已退出登录')
  router.push('/')
}

onMounted(() => {
  loadProfileData()
})
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: end;
}

.page-header h1 {
  margin: 6px 0 8px;
  font-size: 32px;
  color: #2f241d;
}

.subtitle {
  margin: 0;
  color: #6b5b4f;
  max-width: 700px;
}

.page-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  color: #8B4513;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.refresh-btn,
.ghost-btn,
.remove-btn {
  border: none;
  border-radius: 999px;
  padding: 10px 18px;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
}

.refresh-btn {
  background: linear-gradient(135deg, #8B4513 0%, #D4AF37 100%);
  color: #fff;
}

.ghost-btn {
  background: #f7f1e6;
  color: #8B4513;
}

.remove-btn {
  background: #fff0ef;
  color: #b42318;
  white-space: nowrap;
}

.loading-state,
.error-state,
.empty-state,
.modal-card,
.user-card,
.panel,
.stat-card,
.forum-panel {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 48px 24px;
}

.loading-icon,
.error-icon,
.empty-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.user-card {
  padding: 28px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.avatar-wrap {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #f4e4c1;
  flex-shrink: 0;
}

.avatar,
.avatar-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-badge {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  color: #fff;
  box-shadow: inset 0 1px 3px rgba(255, 255, 255, 0.5);
  flex-shrink: 0;
}

.user-label {
  font-size: 12px;
  color: #8B4513;
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.user-info h2 {
  margin: 0;
  font-size: 28px;
  color: #2f241d;
}

.user-id {
  color: #6b5b4f;
  margin: 8px 0 14px;
}

.user-tags {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.user-tag-btn {
  border: 1px solid #eadcc4;
  background: #fffdf8;
  color: #8B4513;
  border-radius: 999px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.user-tag-btn.active {
  background: linear-gradient(135deg, #f4d27a 0%, #d4af37 100%);
  color: #2f241d;
  border-color: transparent;
}

.content-panel {
  padding: 24px;
}

.panel,
.forum-panel {
  padding: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 12px;
  margin-bottom: 18px;
}

.panel-header h3 {
  margin: 6px 0 0;
  color: #2f241d;
}

.panel-count {
  color: #8B4513;
  font-weight: 700;
}

.item-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item-card {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  padding: 16px;
  border-radius: 12px;
  background: #faf7f2;
}

.item-main {
  text-decoration: none;
  color: inherit;
  flex: 1;
}

.item-main h4 {
  margin: 6px 0;
  color: #2f241d;
}

.item-tag {
  margin: 0;
  font-size: 12px;
  color: #8B4513;
  font-weight: 700;
}

.item-summary {
  margin: 0;
  color: #69584d;
  line-height: 1.6;
}

.item-arrow {
  font-size: 24px;
  color: #8B4513;
}

.empty-actions {
  margin-top: 16px;
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.forum-post-card {
  align-items: flex-start;
}

.forum-post-main {
  flex: 1;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
  color: #6b5b4f;
  font-size: 13px;
}

.forum-actions {
  display: flex;
  justify-content: flex-end;
}

.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(26, 20, 15, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
}

.modal-card {
  width: min(560px, 100%);
  padding: 24px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  color: #2f241d;
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 20px;
  color: #6b5b4f;
  cursor: pointer;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field-label {
  font-size: 14px;
  color: #8B4513;
  font-weight: 700;
}

.field-input {
  width: 100%;
  border: 1px solid #e6dccf;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 14px;
  color: #2f241d;
}

.avatar-picker {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.avatar-option {
  border: 1px solid #eadcc4;
  background: #fffdf8;
  border-radius: 14px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2f241d;
  cursor: pointer;
}

.avatar-option.active {
  border-color: #8B4513;
  background: #fff7e6;
}

.avatar-option-swatch {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.avatar-preview {
  display: flex;
  justify-content: center;
  padding: 8px 0 4px;
}

.preview-avatar {
  width: 84px;
  height: 84px;
  font-size: 34px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

@media (max-width: 900px) {
  .page-header,
  .content-grid,
  .stats-grid,
  .avatar-picker {
    grid-template-columns: 1fr;
    display: grid;
  }

  .page-header {
    align-items: start;
  }

  .user-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
