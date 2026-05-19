<template>
  <div class="news">
    <h1 style="font-size:32px; color:#333; margin-bottom:32px;">行业资讯</h1>

    <div v-if="loading" style="text-align:center; padding: 80px 0;">
      <div style="font-size: 48px; margin-bottom: 16px;">⏳</div>
      <p style="color: #999;">加载中...</p>
    </div>

    <div v-else-if="error" style="text-align:center; padding: 80px 0;">
      <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
      <p style="color: #e74c3c;">{{ error }}</p>
      <button @click="fetchData" style="margin-top:16px; padding:8px 24px; border-radius:20px; border:2px solid #8B4513; background:#8B4513; color:white; cursor:pointer;">重新加载</button>
    </div>

    <template v-else>
      <div style="margin-bottom:24px; display:flex; gap:12px; flex-wrap:wrap;">
        <button v-for="t in types" :key="t.id" @click="currentType = t.id"
          :style="{ padding:'8px 20px', borderRadius:'20px', border: currentType===t.id ? '2px solid #8B4513' : '2px solid #ddd',
            background: currentType===t.id ? '#8B4513':'white', color: currentType===t.id ? 'white':'#333', cursor:'pointer', fontSize:'14px' }">
          {{ t.name }}
        </button>
      </div>

      <div v-if="filteredNews.length === 0" style="text-align:center; padding: 60px 0; color: #999;">
        <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
        <p>暂无资讯</p>
      </div>

      <div v-else style="display:flex; flex-direction:column; gap:20px;">
        <router-link v-for="item in filteredNews" :key="item.id" :to="'/news/' + item.id"
          style="background:white; padding:24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); display:flex; gap:20px; text-decoration:none; color:inherit; transition:transform 0.3s;"
          @mouseenter="$event.target.style.transform='translateY(-2px)'"
          @mouseleave="$event.target.style.transform='none'">
          <div style="width:160px; height:120px; background:linear-gradient(135deg, #D4AF37 0%, #8B4513 100%); border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:48px; flex-shrink:0;">{{ item.icon || getTypeIcon(item.type) }}</div>
          <div style="flex:1;">
            <span style="font-size:12px; color:white; background:#8B4513; padding:2px 10px; border-radius:10px;">{{ typeLabel(item.type) }}</span>
            <h3 style="font-size:20px; color:#333; margin:8px 0;">{{ item.title }}</h3>
            <p style="font-size:14px; color:#666; margin-bottom:12px;">{{ item.summary }}</p>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:13px; color:#999;">📅 {{ formatDate(item.publish_time) }} · 👁 {{ formatViews(item.views) }}</span>
              <span style="font-size:13px; color:#8B4513; font-weight:500;">阅读全文 →</span>
            </div>
          </div>
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { newsApi } from '@/api'

const loading = ref(true)
const error = ref(null)
const allNews = ref([])

const types = [
  { id: 'all', name: '全部' },
  { id: 'company', name: '企业动态' },
  { id: 'policy', name: '政策法规' },
  { id: 'trend', name: '行业趋势' },
  { id: 'event', name: '行业活动' }
]
const currentType = ref('all')

const filteredNews = computed(() => {
  if (currentType.value === 'all') return allNews.value
  return allNews.value.filter(n => n.type === currentType.value)
})

const typeLabel = (t) => ({ company:'企业', policy:'政策', trend:'趋势', event:'活动' }[t] || t)
const getTypeIcon = (t) => ({ company:'🏢', policy:'📋', trend:'📈', event:'🎉' }[t] || '📰')
const formatDate = (d) => d ? d.slice(0,10) : ''
const formatViews = (v) => v >= 10000 ? (v/10000).toFixed(1)+'万' : String(v||'')

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const res = await newsApi.getList({ page: 1, page_size: 20 })
    allNews.value = res.data.list || []
  } catch (e) {
    error.value = '数据加载失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>
