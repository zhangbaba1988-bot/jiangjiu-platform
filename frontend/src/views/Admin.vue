<template>
  <div class="admin-page">
    <div class="page-header">
      <div>
        <p class="eyebrow">超级管理员后台</p>
        <h1>内容维护与会员总览</h1>
        <p class="subtitle">登录后即可查看会员数据，并直接维护首页、联系我们和论坛板块内容，权限会立即同步到前台页面。</p>
      </div>
      <div v-if="loggedIn" class="page-actions">
        <button class="refresh-btn" @click="loadMembers">🔄 刷新会员</button>
        <button class="ghost-btn" @click="saveWebsiteContent">💾 保存内容</button>
        <button class="ghost-btn danger" @click="logout">🚪 退出登录</button>
      </div>
    </div>

    <div v-if="!loggedIn" class="login-card">
      <h2>管理员登录</h2>
      <p class="login-tip">默认账号：superadmin，密码：Jiangjiu@2026</p>
      <div class="permission-panel">
        <h3>当前权限</h3>
        <ul>
          <li v-for="permission in permissions" :key="permission">{{ permission }}</li>
        </ul>
      </div>
      <form class="login-form" @submit.prevent="handleLogin">
        <label class="field-label">账号</label>
        <input v-model="loginForm.username" class="field-input" placeholder="请输入管理员账号" />
        <label class="field-label">密码</label>
        <input v-model="loginForm.password" type="password" class="field-input" placeholder="请输入密码" />
        <button class="refresh-btn" type="submit">登录后台</button>
      </form>
      <p v-if="loginError" class="error-text">{{ loginError }}</p>
    </div>

    <div v-else>
      <div v-if="loading" class="loading-state">
        <div class="loading-icon">⏳</div>
        <p>加载中，请稍后...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <p>{{ error }}</p>
        <button class="refresh-btn" @click="loadMembers">重新尝试</button>
      </div>

      <template v-else>
        <section class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ totalMembers }}</div>
            <div class="stat-label">总会员数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ activeMembers }}</div>
            <div class="stat-label">活跃会员</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ totalFavorites }}</div>
            <div class="stat-label">收藏总量</div>
          </div>
        </section>

        <section class="content-panel">
          <div class="panel-header">
            <div>
              <p class="eyebrow">网站内容管理</p>
              <h2>首页、联系我们、论坛内容同步更新</h2>
            </div>
            <button class="ghost-btn" @click="resetWebsiteContent">恢复默认</button>
          </div>

          <div class="editor-grid">
            <div class="editor-card">
              <h3>首页文案</h3>
              <label class="field-label">标题</label>
              <input v-model="editor.hero.title" class="field-input" />
              <label class="field-label">描述</label>
              <textarea v-model="editor.hero.description" class="field-input textarea-input" rows="3" />
              <label class="field-label">按钮文案</label>
              <input v-model="editor.hero.ctaText" class="field-input" />
              <label class="field-label">按钮跳转</label>
              <input v-model="editor.hero.ctaLink" class="field-input" placeholder="例如 /knowledge" />
            </div>

            <div class="editor-card">
              <h3>联系我们信息</h3>
              <label class="field-label">副标题</label>
              <input v-model="editor.contact.subtitle" class="field-input" />
              <label class="field-label">电话</label>
              <input v-model="editor.contact.phone" class="field-input" />
              <label class="field-label">邮箱</label>
              <input v-model="editor.contact.email" class="field-input" />
              <label class="field-label">地址</label>
              <input v-model="editor.contact.address" class="field-input" />
              <label class="field-label">工作时间</label>
              <input v-model="editor.contact.hours" class="field-input" />
              <label class="field-label">说明文案</label>
              <textarea v-model="editor.contact.note" class="field-input textarea-input" rows="3" />
            </div>

            <div class="editor-card wide-card">
              <h3>论坛话题</h3>
              <div v-for="(topic, index) in editor.forum.topics" :key="index" class="topic-editor">
                <label class="field-label">标题</label>
                <input v-model="topic.title" class="field-input" />
                <label class="field-label">分类</label>
                <input v-model="topic.category" class="field-input" />
                <label class="field-label">作者</label>
                <input v-model="topic.author" class="field-input" />
                <label class="field-label">最后活跃</label>
                <input v-model="topic.lastActive" class="field-input" />
                <label class="field-label">回复数</label>
                <input v-model.number="topic.replies" type="number" class="field-input" />
              </div>
              <label class="field-label">论坛简介</label>
              <textarea v-model="editor.forum.subtitle" class="field-input textarea-input" rows="2" />
              <label class="field-label">社区说明</label>
              <textarea v-model="editor.forum.intro" class="field-input textarea-input" rows="3" />
            </div>
          </div>
        </section>

        <section class="member-grid">
          <div v-for="member in members" :key="member.id" class="member-card">
            <div class="member-top">
              <div v-if="isAvatarUrl(member.avatar)" class="member-avatar-wrap">
                <img :src="member.avatar || defaultAvatar" :alt="member.nickname" class="member-avatar" />
              </div>
              <div v-else class="member-avatar-badge" :style="{ background: getAvatarGradient(member.avatar) }">
                <span>{{ getAvatarIcon(member.avatar) }}</span>
              </div>
              <div>
                <h3>{{ member.nickname }}</h3>
                <p>{{ member.email }}</p>
              </div>
              <span class="status-badge" :class="member.status">{{ member.status === 'active' ? '活跃' : '未激活' }}</span>
            </div>
            <div class="member-details">
              <div>
                <span>注册时间</span>
                <strong>{{ formatTime(member.register_time) }}</strong>
              </div>
              <div>
                <span>最后登录</span>
                <strong>{{ formatTime(member.last_login) }}</strong>
              </div>
              <div>
                <span>收藏数</span>
                <strong>{{ member.favorite_count || 0 }}</strong>
              </div>
              <div>
                <span>浏览历史</span>
                <strong>{{ member.history_count || 0 }}</strong>
              </div>
            </div>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { adminApi } from '@/api'
import { defaultSiteContent, loadSiteContent, saveSiteContent } from '@/utils/siteContent'

const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=jiangjiu'
const avatarOptions = [
  { key: 'amber', label: '金黄', icon: '🍶', gradient: 'linear-gradient(135deg, #F4D27A 0%, #B27818 100%)' },
  { key: 'brown', label: '棕韵', icon: '🍂', gradient: 'linear-gradient(135deg, #A56A3B 0%, #5B2F18 100%)' },
  { key: 'green', label: '青翠', icon: '🌿', gradient: 'linear-gradient(135deg, #8CCB8C 0%, #2F6B4B 100%)' },
  { key: 'blue', label: '湖蓝', icon: '🌊', gradient: 'linear-gradient(135deg, #86C8E6 0%, #235E8B 100%)' }
]

const loggedIn = ref(false)
const loading = ref(false)
const error = ref('')
const loginError = ref('')
const members = ref([])
const loginForm = ref({
  username: 'superadmin',
  password: 'Jiangjiu@2026'
})
const editor = ref(loadSiteContent())
const permissions = ref(defaultSiteContent().permissions)

const isAvatarUrl = (value) => typeof value === 'string' && /^https?:\/\//i.test(value)

const getAvatarOption = (value) => {
  const normalized = value || 'amber'
  return avatarOptions.find(option => option.key === normalized) || avatarOptions[0]
}

const getAvatarGradient = (value) => getAvatarOption(value).gradient

const getAvatarIcon = (value) => getAvatarOption(value).icon

const totalMembers = computed(() => members.value.length)
const activeMembers = computed(() => members.value.filter(item => item.status === 'active').length)
const totalFavorites = computed(() => members.value.reduce((sum, member) => sum + (member.favorite_count || 0), 0))

const loadMembers = async () => {
  loading.value = true
  error.value = ''

  try {
    const res = await adminApi.getMembers()
    members.value = res.data.members || []
  } catch (e) {
    error.value = '获取会员数据失败，请检查后台登录状态'
  } finally {
    loading.value = false
  }
}

const handleLogin = async () => {
  loginError.value = ''

  try {
    const res = await adminApi.login(loginForm.value)
    localStorage.setItem('adminToken', res.data.token)
    loggedIn.value = true
    editor.value = loadSiteContent()
    ElMessage.success('管理员登录成功')
    await loadMembers()
  } catch (e) {
    loginError.value = '管理员账号或密码错误'
  }
}

const saveWebsiteContent = () => {
  saveSiteContent(editor.value)
  ElMessage.success('网站内容已更新')
}

const resetWebsiteContent = () => {
  editor.value = defaultSiteContent()
  saveSiteContent(editor.value)
  ElMessage.info('已恢复默认内容')
}

const formatTime = (value) => {
  if (!value) return '--'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('zh-CN')
}

const logout = () => {
  localStorage.removeItem('adminToken')
  loggedIn.value = false
  members.value = []
  ElMessage.success('已退出管理员后台')
}

onMounted(() => {
  const token = localStorage.getItem('adminToken')
  loggedIn.value = !!token
  editor.value = loadSiteContent()
  if (loggedIn.value) {
    loadMembers()
  }
})
</script>

<style scoped>
.admin-page {
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
  max-width: 760px;
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

.login-card,
.loading-state,
.error-state,
.stat-card,
.member-card,
.content-panel,
.editor-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
}

.login-card {
  padding: 28px;
  max-width: 760px;
}

.login-tip {
  color: #6b5b4f;
  margin: 8px 0 20px;
}

.permission-panel {
  background: #fff9ee;
  border-radius: 16px;
  padding: 18px 20px;
  margin-bottom: 20px;
}

.permission-panel h3 {
  margin-bottom: 12px;
  color: #8B4513;
}

.permission-panel ul {
  padding-left: 18px;
  color: #4d413a;
  line-height: 1.8;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field-label {
  font-size: 14px;
  color: #8B4513;
  font-weight: 700;
  margin-top: 12px;
}

.field-input {
  width: 100%;
  border: 1px solid #e6dccf;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 14px;
  color: #2f241d;
  font-family: inherit;
}

.textarea-input {
  min-height: 110px;
  resize: vertical;
}

.refresh-btn,
.ghost-btn {
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

.ghost-btn.danger {
  background: #fff2f2;
  color: #b42318;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 48px 24px;
}

.loading-icon,
.error-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.stat-card {
  padding: 24px;
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: 800;
  color: #8B4513;
}

.stat-label {
  margin-top: 8px;
  color: #6b5b4f;
}

.content-panel {
  padding: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h2 {
  margin-top: 6px;
  color: #2f241d;
}

.editor-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.editor-card {
  padding: 20px;
}

.editor-card h3 {
  margin-bottom: 8px;
  color: #2f241d;
}

.wide-card {
  grid-column: 1 / -1;
}

.topic-editor {
  padding: 14px 0;
  border-top: 1px dashed #ead8bd;
}

.topic-editor:first-of-type {
  border-top: none;
}

.member-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.member-card {
  padding: 20px;
}

.member-top {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 16px;
}

.member-top h3 {
  margin: 0 0 4px;
  color: #2f241d;
}

.member-top p {
  margin: 0;
  color: #6b5b4f;
}

.member-avatar-wrap {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #f4e4c1;
  flex-shrink: 0;
}

.member-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-avatar-badge {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  flex-shrink: 0;
}

.status-badge {
  margin-left: auto;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 700;
}

.status-badge.active {
  background: #eefbf3;
  color: #0f9f4a;
}

.status-badge.inactive {
  background: #fff5e6;
  color: #a65b0d;
}

.member-details {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.member-details div {
  padding: 12px;
  border-radius: 12px;
  background: #faf7f2;
}

.member-details span {
  display: block;
  font-size: 12px;
  color: #8B4513;
  margin-bottom: 6px;
}

.member-details strong {
  color: #2f241d;
}

.error-text {
  margin-top: 12px;
  color: #b42318;
}

@media (max-width: 900px) {
  .page-header,
  .stats-grid,
  .member-grid,
  .member-details,
  .editor-grid {
    grid-template-columns: 1fr;
    display: grid;
  }

  .page-header {
    align-items: start;
  }

  .panel-header,
  .member-top {
    align-items: flex-start;
  }
}
</style>
