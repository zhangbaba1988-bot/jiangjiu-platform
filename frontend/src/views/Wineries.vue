<template>
  <div class="wineries">
    <h1 class="page-title">酒厂名录</h1>

    <div v-if="loading" class="state-box">
      <span>⏳ 加载中...</span>
    </div>
    <div v-else-if="error" class="state-box error">
      <span>{{ error }}</span>
      <button @click="fetchData" class="retry-btn">重试</button>
    </div>

    <template v-else>
      <!-- 概览统计 -->
      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-val">{{ allWineries.length }}</span>
          <span class="stat-label">收录酒厂</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">{{ regions.length - 1 }}</span>
          <span class="stat-label">覆盖产区</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">{{ totalOutput > 0 ? formatNum(totalOutput) + '万吨' : '—' }}</span>
          <span class="stat-label">总年产能</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">{{ oldestYear }}</span>
          <span class="stat-label">最早建厂</span>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-box">
        <input v-model="searchQuery" type="text" placeholder="搜索酒厂名称、品牌、产区..." class="search-input" />
        <span class="search-count" v-if="searchQuery">{{ filteredWineries.length }} 条结果</span>
      </div>

      <!-- 产区筛选 -->
      <div class="filter-bar">
        <button v-for="r in regions" :key="r" @click="currentRegion = r; goPage(1)"
          :class="['filter-btn', { active: currentRegion === r }]">
          {{ r }} ({{ countByRegion(r) }})
        </button>
      </div>

      <!-- 分页信息 -->
      <div class="page-info">
        <span>共 {{ filteredWineries.length }} 家酒厂，每页 {{ pageSize }} 家</span>
      </div>

      <!-- 酒厂列表 -->
      <div class="winery-list">
        <router-link v-for="w in pagedWineries" :key="w.id" :to="'/wineries/' + w.id" class="winery-row">
          <img v-if="isImageIcon(w.icon)" :src="baseUrl + w.icon" class="w-icon-img" alt="" />
          <span v-else class="w-icon">{{ w.icon || '🏭' }}</span>
          <div class="w-body">
            <div class="w-top">
              <span class="w-name">{{ w.name }}</span>
              <span class="w-year">{{ w.established }}年</span>
            </div>
            <div class="w-bottom">
              <span class="w-desc">{{ w.description }}</span>
              <span class="w-meta">{{ w.production }} · {{ w.brand }} · 年产{{ formatOutput(w.annual_output) }}</span>
            </div>
          </div>
          <span class="w-arrow">›</span>
        </router-link>
      </div>

      <!-- 分页器 -->
      <div class="pagination-bar" v-if="totalPages > 1">
        <button class="page-btn" :disabled="currentPage <= 1" @click="goPage(currentPage - 1)">‹ 上一页</button>
        <button v-for="p in visiblePages" :key="p" :class="['page-btn', { active: p === currentPage }]" @click="goPage(p)">
          {{ p }}
        </button>
        <button class="page-btn" :disabled="currentPage >= totalPages" @click="goPage(currentPage + 1)">下一页 ›</button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const baseUrl = import.meta.env.BASE_URL
import { wineryApi } from '@/api'

const loading = ref(true)
const error = ref(null)
const allWineries = ref([])
const currentRegion = ref('全部')
const searchQuery = ref('')

const regions = computed(() => {
  const set = new Set(allWineries.value.map(w => w.production))
  return ['全部', ...Array.from(set)]
})

const pageSize = 50
const currentPage = ref(1)

const filteredWineries = computed(() => {
  let list = allWineries.value
  if (currentRegion.value !== '全部') {
    list = list.filter(w => w.production === currentRegion.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter(w => 
      w.name.toLowerCase().includes(q) ||
      (w.brand && w.brand.toLowerCase().includes(q)) ||
      w.production.toLowerCase().includes(q) ||
      (w.description && w.description.toLowerCase().includes(q))
    )
  }
  return list
})

const totalPages = computed(() => Math.ceil(filteredWineries.value.length / pageSize))

const pagedWineries = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredWineries.value.slice(start, start + pageSize)
})

const visiblePages = computed(() => {
  const total = totalPages.value
  const cur = currentPage.value
  if (total <= 7) return Array.from({length: total}, (_, i) => i + 1)
  if (cur <= 4) return [1,2,3,4,5, '...', total]
  if (cur >= total - 3) return [1, '...', total-4, total-3, total-2, total-1, total]
  return [1, '...', cur-1, cur, cur+1, '...', total]
})

const goPage = (p) => {
  if (typeof p === 'number' && p >= 1 && p <= totalPages.value) {
    currentPage.value = p
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const countByRegion = (r) => {
  if (r === '全部') return allWineries.value.length
  return allWineries.value.filter(w => w.production === r).length
}

const totalOutput = computed(() => allWineries.value.reduce((s,w) => s + (w.annual_output||0), 0))
const oldestYear = computed(() => {
  const years = allWineries.value.map(w => parseInt(w.established)||9999)
  return Math.min(...years)
})
const formatNum = (n) => (n/10000).toFixed(1)
// 判断icon是否为图片路径
const isImageIcon = (icon) => icon && (icon.startsWith('/') || icon.startsWith('http'))

const formatOutput = (n) => {
  if (n === null || n === undefined || n === 0) return '数据不详'
  if (n >= 10000) return (n/10000).toFixed(1) + '万吨'
  return (n/1000).toFixed(0) + '千吨'
}

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const res = await wineryApi.getList({ page: 1, page_size: 500 })
    allWineries.value = res.data.list || []
  } catch (e) {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.page-title { font-size: 24px; color: #333; margin-bottom: 20px; font-weight: 600; }

.stats-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.stat-item { flex:1; text-align:center; padding:14px 8px; background:#fff; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.stat-val { display:block; font-size:20px; font-weight:700; color:#8B4513; margin-bottom:3px; }
.stat-label { font-size:12px; color:#999; }

.search-box { display:flex; align-items:center; gap:10px; margin-bottom:14px; }
.search-input {
  flex:1; padding:10px 16px; border-radius:20px; border:1px solid #e0e0e0;
  font-size:14px; outline:none; transition:border .2s;
}
.search-input:focus { border-color:#8B4513; }
.search-count { font-size:13px; color:#8B4513; white-space:nowrap; }

.state-box {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 14px;
}
.state-box.error { color: #e74c3c; }
.retry-btn {
  margin-top: 12px; padding: 6px 20px; border-radius: 16px;
  border: 1px solid #8B4513; background: #8B4513; color: #fff; cursor: pointer; font-size: 13px;
}

/* 产区筛选 */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.filter-btn {
  padding: 5px 16px;
  border-radius: 16px;
  border: 1px solid #e0e0e0;
  background: #fff;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-btn:hover { border-color: #8B4513; color: #8B4513; }
.filter-btn.active {
  background: #8B4513;
  color: #fff;
  border-color: #8B4513;
}

/* 紧凑列表 */
.winery-list {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
}
.winery-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-bottom: 1px solid #f5f5f5;
  text-decoration: none;
  color: inherit;
  transition: background 0.15s;
}
.winery-row:last-child { border-bottom: none; }
.winery-row:hover { background: #faf8f5; }

.w-icon {
  font-size: 28px;
  width: 40px;
  height: 40px;
  text-align: center;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.w-icon-img {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: contain;
  flex-shrink: 0;
}
.w-body {
  flex: 1;
  min-width: 0;
}
.w-top {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 3px;
}
.w-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}
.w-year {
  font-size: 12px;
  color: #999;
  flex-shrink: 0;
}
.w-bottom {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.w-desc {
  font-size: 13px;
  color: #8B4513;
  flex-shrink: 0;
}
.w-meta {
  font-size: 12px;
  color: #bbb;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.w-arrow {
  font-size: 18px;
  color: #ccc;
  flex-shrink: 0;
}

/* 分页信息 */
.page-info {
  text-align: right;
  margin: 12px 0 8px;
  font-size: 13px;
  color: #999;
}

/* 分页器 */
.pagination-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin: 24px 0 40px;
  flex-wrap: wrap;
}
.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fff;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.page-btn:hover:not(:disabled) {
  border-color: #8B4513;
  color: #8B4513;
}
.page-btn.active {
  background: #8B4513;
  color: #fff;
  border-color: #8B4513;
}
.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
