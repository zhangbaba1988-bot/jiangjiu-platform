<template>
  <div class="winery-detail">
    <button class="back-btn" @click="$router.back()">← 返回酒厂名录</button>

    <div v-if="loading" class="state-box"><span>⏳ 加载中...</span></div>
    <div v-else-if="error" class="state-box error"><span>{{ error }}</span></div>

    <article v-else class="detail-card">
      <!-- 头部 -->
      <header class="w-header">
        <img v-if="w.icon && (w.icon.startsWith('/') || w.icon.startsWith('http'))" :src="baseUrl + w.icon" class="w-icon-lg" alt="" />
        <span v-else class="w-icon-lg">{{ w.icon || '🏭' }}</span>
        <div>
          <h1>{{ w.name }}</h1>
          <p class="w-brand">{{ w.brand }} · {{ w.established }}年成立</p>
        </div>
      </header>

      <!-- 核心数据 -->
      <div class="stats-row">
        <div class="stat">
          <span class="stat-val">{{ formatOutput(w.annual_output) }}</span>
          <span class="stat-label">年产量</span>
        </div>
        <div class="stat">
          <span class="stat-val">{{ w.production }}</span>
          <span class="stat-label">所在产区</span>
        </div>
        <div class="stat">
          <span class="stat-val">{{ w.established }}年</span>
          <span class="stat-label">建厂年份</span>
        </div>
      </div>

      <!-- 官网链接 -->
      <div class="website-bar" v-if="w.website">
        <a :href="w.website" target="_blank" rel="noopener noreferrer" class="website-link">
          <span class="website-icon">🌐</span>
          <span>官方网站：{{ w.website }}</span>
          <span class="website-arrow">↗</span>
        </a>
      </div>

      <!-- 企业简介 -->
      <section class="section">
        <h3>企业简介</h3>
        <p>{{ w.description }}</p>
      </section>

      <!-- 企业故事 -->
      <section class="section" v-if="w.story">
        <h3>发展历程</h3>
        <p>{{ w.story }}</p>
      </section>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { wineryApi } from '@/api'

const route = useRoute()
const router = useRouter()
const baseUrl = import.meta.env.BASE_URL

const formatOutput = (n) => {
  if (n === null || n === undefined || n === 0) return '数据不详'
  if (n >= 10000) return (n/10000).toFixed(1) + '万吨'
  return (n/1000).toFixed(0) + '千吨'
}

const loading = ref(true)
const error = ref(null)
const w = ref({})

onMounted(async () => {
  try {
    const res = await wineryApi.getDetail(route.params.id)
    if (res.code === 200 && res.data) w.value = res.data
    else error.value = '酒厂信息不存在'
  } catch (e) {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.winery-detail {
  max-width: 680px;
  margin: 0 auto;
  padding: 20px 16px 60px;
}

.back-btn {
  display: inline-flex;
  align-items: center; gap: 4px;
  background: none; border: 1px solid #ddd;
  padding: 6px 18px; border-radius: 18px;
  color: #666; font-size: 13px; cursor: pointer;
  margin-bottom: 20px; transition: all 0.2s;
}
.back-btn:hover { border-color: #8B4513; color: #8B4513; }

.state-box { text-align: center; padding: 80px 0; color: #999; font-size: 14px; }
.state-box.error { color: #e74c3c; }

.detail-card {
  background: #fff; border-radius: 12px;
  padding: 36px 36px 40px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.w-header {
  display: flex; align-items: center; gap: 20px;
  margin-bottom: 28px; padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}
.w-icon-lg {
  width: 72px;
  height: 72px;
  object-fit: contain;
  border-radius: 12px;
  flex-shrink: 0;
}
.w-header h1 { font-size: 24px; color: #1a1a1a; margin: 0 0 4px; font-weight: 700; }
.w-brand { font-size: 14px; color: #999; margin: 0; }

.stats-row {
  display: flex; gap: 12px; margin-bottom: 28px;
}
.stat {
  flex: 1; text-align: center;
  padding: 16px 8px;
  background: #faf8f5; border-radius: 8px;
}
.stat-val { display: block; font-size: 18px; font-weight: 700; color: #8B4513; margin-bottom: 4px; }
.stat-label { font-size: 12px; color: #999; }

.website-bar {
  margin-bottom: 20px;
}
.website-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #f5f0eb;
  border: 1px solid #e0d5c8;
  border-radius: 10px;
  color: #8B4513;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s;
}
.website-link:hover {
  background: #ede4d8;
  border-color: #D4AF37;
}
.website-icon { font-size: 16px; }
.website-arrow { font-size: 14px; opacity: 0.6; }

.section {
  margin-top: 24px;
}
.section h3 {
  font-size: 16px; font-weight: 600; color: #8B4513;
  padding-left: 10px; border-left: 3px solid #D4AF37;
  margin: 0 0 10px;
}
.section p {
  font-size: 15px; line-height: 1.8; color: #555; margin: 0;
}
</style>
