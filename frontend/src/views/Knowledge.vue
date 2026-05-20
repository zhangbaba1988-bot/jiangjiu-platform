<template>
  <div class="knowledge">
    <h1 style="font-size:32px; color:#333; margin-bottom:16px;">酱酒知识库</h1>

    <!-- Loading -->
    <div v-if="loading" style="text-align:center; padding: 80px 0;">
      <div style="font-size: 48px; margin-bottom: 16px;">⏳</div>
      <p style="color: #999; font-size: 16px;">加载中...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" style="text-align:center; padding: 80px 0;">
      <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
      <p style="color: #e74c3c; font-size: 16px;">{{ error }}</p>
      <button @click="fetchData" style="margin-top:16px; padding:8px 24px; border-radius:20px; border:2px solid #8B4513; background:#8B4513; color:white; cursor:pointer;">重新加载</button>
    </div>

    <template v-else>
      <div style="margin-bottom:32px; display:flex; gap:12px; flex-wrap:wrap;">
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="currentCategory = cat.id"
          :style="{
            padding: '10px 24px',
            borderRadius: '20px',
            border: currentCategory === cat.id ? '2px solid #8B4513' : '2px solid #ddd',
            background: currentCategory === cat.id ? '#8B4513' : 'white',
            color: currentCategory === cat.id ? 'white' : '#333',
            cursor: 'pointer',
            fontSize: '14px'
          }"
        >
          {{ cat.name }} ({{ getArticleCount(cat.id) }})
        </button>
      </div>
      
      <div v-if="currentArticles.length === 0" style="text-align:center; padding: 60px 0; color: #999;">
        <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
        <p>暂无内容</p>
      </div>

      <div v-else class="article-list">
        <router-link 
          v-for="article in currentArticles" 
          :key="article.id" 
          :to="'/knowledge/' + article.id" 
          class="article-row"
        >
          <span class="a-icon">{{ article.icon || getIcon(article.category) }}</span>
          <div class="a-body">
            <span class="a-title">{{ article.title }}</span>
            <span class="a-summary">{{ article.summary }}</span>
          </div>
          <span class="a-meta">{{ formatViews(article.views) }} 阅读</span>
        </router-link>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { knowledgeApi } from '@/api'

const loading = ref(true)
const error = ref(null)
const allArticles = ref([])

const categories = [
  { id: 'all', name: '全部' },
  { id: 'culture', name: '酱酒文化' },
  { id: 'craft', name: '酿造工艺' },
  { id: 'tasting', name: '品鉴收藏' },
  { id: 'industry', name: '行业知识' }
]

const currentCategory = ref('all')

const currentArticles = computed(() => {
  if (currentCategory.value === 'all') {
    return allArticles.value
  }
  return allArticles.value.filter(a => a.category === currentCategory.value)
})

const getArticleCount = (catId) => {
  if (catId === 'all') {
    return allArticles.value.length
  }
  return allArticles.value.filter(a => a.category === catId).length
}

const getIcon = (category) => {
  const icons = { culture: '📜', craft: '📖', tasting: '👃' }
  return icons[category] || '📄'
}

const formatViews = (views) => {
  if (views >= 10000) {
    return (views / 10000).toFixed(1) + '万'
  }
  return String(views)
}

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const res = await knowledgeApi.getList({ page: 1, page_size: 50 })
    allArticles.value = res.data.list || []
  } catch (e) {
    allArticles.value = [
      { id: 'klg_043', title: '抖音金黄桶装酱酒是真老酒吗？新国标说清楚了', category: 'tasting', icon: '🛢️', summary: '新国标GB/T 10781.4-2024明确：正宗酱酒无色或微黄，严禁添加焦糖色。抖音塑料桶金黄酱酒多为新酒+人工色素。', views: 5800 },
      { id: 'klg_014', title: '坤沙、翻沙、碎沙、窜沙：酱酒的四种工艺等级', category: 'craft', icon: '📊', summary: '正确的酱酒等级排列：坤沙第一 > 翻沙第二 > 碎沙第三 > 窜沙第四。翻沙是坤沙的延续，碎沙工艺完全不同', views: 16789 },
      { id: 'klg_011', title: '12987工艺详解：酱酒酿造的核心密码', category: 'craft', icon: '📖', summary: '一年周期、两次投料、九次蒸煮、八次发酵、七次取酒——完整解析坤沙酱酒工艺', views: 18765 },
      { id: 'klg_001', title: '酱酒历史溯源：从远古到现代的千年传承', category: 'culture', icon: '📜', summary: '深入探索酱酒的起源与发展，从汉武帝枸酱酒到巴拿马金奖的传奇故事', views: 15678 }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.article-list {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
}
.article-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 18px;
  border-bottom: 1px solid #f5f5f5;
  text-decoration: none;
  color: inherit;
  transition: background 0.15s;
}
.article-row:last-child { border-bottom: none; }
.article-row:hover { background: #faf8f5; }
.a-icon { font-size: 26px; width: 36px; text-align: center; flex-shrink: 0; }
.a-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.a-title { font-size: 14px; font-weight: 600; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.a-summary { font-size: 12px; color: #999; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.a-meta { font-size: 11px; color: #bbb; flex-shrink: 0; white-space: nowrap; }
</style>
