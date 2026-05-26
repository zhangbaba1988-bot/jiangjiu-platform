<template>
  <div class="forum-page">
    <section class="forum-hero">
      <div>
        <p class="eyebrow">论坛板块</p>
        <h1>{{ content.title }}</h1>
        <p class="hero-copy">{{ content.subtitle }}</p>
        <p class="hero-note">{{ content.intro }}</p>
      </div>

      <div class="hero-status-box">
        <p class="panel-label">发帖校验</p>
        <h2>{{ isLoggedIn ? '已登录，可发布话题' : '未登录，暂不可发布话题' }}</h2>
        <p>{{ isLoggedIn ? '你现在可以直接发起讨论，帖子会保存在当前浏览器中。' : '请先在个人中心确认登录状态后再发布话题。' }}</p>
        <button class="ghost-btn" @click="goToProfile">前往个人中心</button>
      </div>
    </section>

    <section class="summary-grid">
      <div class="summary-card">
        <strong>{{ forumTopics.length }}</strong>
        <span>活跃话题</span>
      </div>
      <div class="summary-card">
        <strong>{{ totalReplies }}</strong>
        <span>累计回复</span>
      </div>
      <div class="summary-card">
        <strong>{{ isLoggedIn ? '已登录' : '未登录' }}</strong>
        <span>当前状态</span>
      </div>
    </section>

    <section class="forum-layout">
      <div class="composer-card">
        <div class="composer-header">
          <div>
            <p class="eyebrow">发帖窗口</p>
            <h2>发布新的讨论</h2>
          </div>
          <span class="status-pill" :class="isLoggedIn ? 'online' : 'offline'">{{ isLoggedIn ? '可发布' : '需登录' }}</span>
        </div>

        <div class="composer-grid">
          <label>
            标题
            <input v-model="draft.title" type="text" placeholder="输入讨论标题" maxlength="80" />
          </label>

          <label>
            分类
            <select v-model="draft.category">
              <option>品鉴交流</option>
              <option>内容合作</option>
              <option>政策解读</option>
              <option>产区讨论</option>
            </select>
          </label>
        </div>

        <label>
          内容
          <textarea v-model="draft.content" rows="6" placeholder="写下你的观点、问题或经验分享"></textarea>
        </label>

        <div class="composer-actions">
          <button class="primary-btn" @click="submitTopic">{{ isLoggedIn ? '发布话题' : '登录后发布' }}</button>
          <button class="secondary-btn" @click="resetDraft">清空内容</button>
        </div>
      </div>

      <aside class="sidebar-stack">
        <div class="sidebar-card">
          <p class="eyebrow">社区规则</p>
          <h3>建议的讨论方式</h3>
          <ul>
            <li>优先描述问题背景与实际场景</li>
            <li>保留清晰的观点与可执行建议</li>
            <li>避免广告与无关内容，维护良好社区氛围</li>
          </ul>
        </div>

        <div class="sidebar-card">
          <p class="eyebrow">版块说明</p>
          <h3>你可以在这里讨论</h3>
          <ul>
            <li>酱酒品鉴心得与收藏建议</li>
            <li>产区文化与品牌传播思路</li>
            <li>行业政策与新标准解读</li>
          </ul>
        </div>
      </aside>
    </section>

    <section class="thread-section">
      <div class="thread-header">
        <div>
          <p class="eyebrow">热门讨论</p>
          <h2>社区最新话题</h2>
        </div>
        <p class="section-note">帖子会保存在当前浏览器中，方便你持续查看与回访。</p>
      </div>

      <div class="thread-list">
        <article v-for="topic in forumTopics" :key="topic.id" class="thread-card">
          <div class="thread-top">
            <span class="topic-tag">{{ topic.category }}</span>
            <span class="reply-pill">{{ topic.replies }} 回复</span>
          </div>
          <h3>{{ topic.title }}</h3>
          <p class="thread-content">{{ topic.content }}</p>
          <div class="thread-meta">
            <span>作者：{{ topic.author }}</span>
            <span>时间：{{ topic.createdAt }}</span>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { loadSiteContent } from '@/utils/siteContent'

const router = useRouter()
const content = ref(loadSiteContent().forum)
const storageKey = 'jiangjiu_forum_posts'
const isLoggedIn = ref(false)

const refreshLoginState = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

const buildTopic = (topic, fallbackReply = 0) => ({
  id: topic.id || `${Date.now()}-${Math.random().toString(16).slice(2)}`,
  title: topic.title,
  category: topic.category,
  author: topic.author,
  content: topic.content || topic.summary || '',
  replies: topic.replies ?? fallbackReply,
  createdAt: topic.createdAt || '刚刚'
})

const defaultTopics = [
  buildTopic({
    title: '如何判断一款酱酒是否适合长期收藏？',
    category: '品鉴交流',
    author: '老酒收藏者',
    content: '分享你在选择藏酒时的判断标准，以及哪些特征最值得关注。',
    replies: 18,
    createdAt: '2小时前'
  }, 18),
  buildTopic({
    title: '品牌方如何做好产区文化内容运营？',
    category: '内容合作',
    author: '内容运营专员',
    content: '围绕产区故事、品牌认知与社群运营，谈谈你们的经验。',
    replies: 11,
    createdAt: '今天 10:30'
  }, 11),
  buildTopic({
    title: '新国标对传统工艺与市场营销有哪些影响？',
    category: '政策解读',
    author: '行业观察员',
    content: '结合最新标准，讨论对工艺传承与市场表达的影响。',
    replies: 9,
    createdAt: '昨天'
  }, 9)
]

const forumTopics = ref([])
const draft = ref({
  title: '',
  category: '品鉴交流',
  content: ''
})

const totalReplies = computed(() => forumTopics.value.reduce((sum, topic) => sum + (topic.replies || 0), 0))

const saveTopics = () => {
  localStorage.setItem(storageKey, JSON.stringify(forumTopics.value))
}

const resetDraft = () => {
  draft.value = {
    title: '',
    category: '品鉴交流',
    content: ''
  }
}

const goToProfile = () => {
  router.push('/profile')
}

const submitTopic = () => {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录后再发布话题，当前可前往个人中心检查登录状态。')
    return
  }

  if (!draft.value.title.trim() || !draft.value.content.trim()) {
    ElMessage.warning('请补充话题标题和内容后再发布。')
    return
  }

  forumTopics.value.unshift({
    id: `${Date.now()}`,
    title: draft.value.title.trim(),
    category: draft.value.category,
    author: '当前用户',
    content: draft.value.content.trim(),
    replies: 0,
    createdAt: '刚刚'
  })

  saveTopics()
  resetDraft()
  ElMessage.success('话题已发布，已保存到当前浏览器。')
}

onMounted(() => {
  refreshLoginState()
  content.value = loadSiteContent().forum

  const saved = localStorage.getItem(storageKey)
  try {
    if (saved) {
      const parsed = JSON.parse(saved)
      forumTopics.value = Array.isArray(parsed) && parsed.length ? parsed : [...defaultTopics]
    } else {
      forumTopics.value = [...defaultTopics]
      saveTopics()
    }
  } catch (error) {
    console.warn('论坛数据解析失败，已恢复默认话题', error)
    forumTopics.value = [...defaultTopics]
    saveTopics()
  }

  window.addEventListener('storage', refreshLoginState)
})

onBeforeUnmount(() => {
  window.removeEventListener('storage', refreshLoginState)
})
</script>

<style scoped>
.forum-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.forum-hero,
.composer-card,
.sidebar-card,
.summary-card,
.thread-card,
.hero-status-box {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 12px 30px rgba(139, 69, 19, 0.1);
}

.forum-hero {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
  padding: 32px;
  align-items: stretch;
}

.forum-hero h1 {
  margin: 8px 0 12px;
  font-size: 32px;
  color: #2f241d;
}

.hero-copy,
.hero-note {
  color: #66584d;
  line-height: 1.8;
}

.hero-status-box {
  padding: 24px;
}

.panel-label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 12px;
  font-weight: 800;
  color: #8B4513;
  margin-bottom: 8px;
}

.hero-status-box h2 {
  font-size: 22px;
  color: #2f241d;
  margin-bottom: 10px;
}

.hero-status-box p {
  color: #66584d;
  line-height: 1.8;
  margin-bottom: 16px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.summary-card {
  padding: 22px;
  text-align: center;
}

.summary-card strong {
  display: block;
  font-size: 28px;
  color: #8B4513;
  margin-bottom: 8px;
}

.summary-card span {
  color: #66584d;
}

.forum-layout {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 20px;
}

.composer-card,
.sidebar-card,
.thread-card {
  padding: 24px;
}

.composer-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: start;
  margin-bottom: 18px;
}

.composer-header h2,
.thread-header h2 {
  margin-top: 8px;
  color: #2f241d;
}

.status-pill {
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 800;
}

.status-pill.online {
  background: #edfdf1;
  color: #0f9f4a;
}

.status-pill.offline {
  background: #fff5e6;
  color: #a65b0d;
}

.composer-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.composer-card label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: #8B4513;
  margin-top: 14px;
}

.composer-card input,
.composer-card select,
.composer-card textarea {
  border: 1px solid #e6dccf;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 14px;
  font-family: inherit;
  color: #2f241d;
}

.composer-card textarea {
  resize: vertical;
  min-height: 120px;
}

.composer-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.primary-btn,
.secondary-btn,
.ghost-btn {
  border: none;
  border-radius: 999px;
  padding: 12px 18px;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
}

.primary-btn {
  background: linear-gradient(135deg, #8B4513 0%, #D4AF37 100%);
  color: #fff;
}

.secondary-btn,
.ghost-btn {
  background: #f7f1e6;
  color: #8B4513;
}

.sidebar-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-card h3 {
  margin: 8px 0 12px;
  color: #2f241d;
}

.sidebar-card ul {
  padding-left: 18px;
  color: #66584d;
  line-height: 1.9;
}

.thread-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.thread-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: end;
}

.section-note {
  max-width: 520px;
  color: #66584d;
  line-height: 1.8;
}

.thread-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.thread-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.topic-tag,
.reply-pill {
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  padding: 5px 10px;
}

.topic-tag {
  background: #f7f1e6;
  color: #8B4513;
}

.reply-pill {
  background: #fff6d8;
  color: #8b5d0a;
}

.thread-card h3 {
  color: #2f241d;
  font-size: 18px;
  margin-bottom: 10px;
}

.thread-content {
  color: #66584d;
  line-height: 1.8;
  margin-bottom: 16px;
}

.thread-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #7e6758;
  font-size: 13px;
}

@media (max-width: 900px) {
  .forum-hero,
  .forum-layout,
  .summary-grid,
  .thread-list,
  .composer-grid,
  .thread-header {
    grid-template-columns: 1fr;
    display: grid;
  }

  .thread-header {
    align-items: start;
  }
}

@media (max-width: 767px) {
  .forum-hero,
  .composer-card,
  .sidebar-card,
  .summary-card,
  .thread-card,
  .hero-status-box {
    padding: 22px;
  }
}
</style>
