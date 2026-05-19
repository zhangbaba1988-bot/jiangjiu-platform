<template>
  <div class="production">
    <h1 class="page-title">中国酱酒产区分布</h1>

    <div v-if="loading" class="state-box"><span>⏳ 加载中...</span></div>
    <div v-else-if="error" class="state-box error"><span>{{ error }}</span><button @click="fetchData" class="retry-btn">重试</button></div>

    <template v-else>
      <!-- 概览统计 -->
      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-val">{{ totalRegions }}</span>
          <span class="stat-label">产区数量</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">{{ formatNum(totalOutput) }}吨</span>
          <span class="stat-label">年总产量</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">{{ totalValue }}亿</span>
          <span class="stat-label">年总产值</span>
        </div>
        <div class="stat-item">
          <span class="stat-val">{{ formatNum(totalWineries) }}家</span>
          <span class="stat-label">酒厂数量</span>
        </div>
      </div>

      <!-- 地图区域 -->
      <div class="map-card">
        <h2>赤水河流域酱酒产区分布图</h2>
        <div class="map-area">
          <svg viewBox="0 0 800 400" class="river-map">
            <!-- 背景 -->
            <rect width="800" height="400" fill="#faf8f0" rx="8"/>
            
            <!-- 赤水河主线 -->
            <path d="M 60,160 C 130,140 180,120 230,150 S 280,190 330,170 S 400,160 440,180 S 500,200 550,190 S 620,180 670,195 S 720,200 760,210"
              fill="none" stroke="#48a9e6" stroke-width="4" stroke-linecap="round"/>
            <path d="M 60,160 C 130,140 180,120 230,150 S 280,190 330,170 S 400,160 440,180 S 500,200 550,190 S 620,180 670,195 S 720,200 760,210"
              fill="none" stroke="#7ec8e3" stroke-width="8" stroke-linecap="round" opacity="0.3"/>
            
            <!-- 支流 -->
            <path d="M 230,150 C 250,210 270,260 290,310" fill="none" stroke="#a0d2db" stroke-width="2" stroke-dasharray="4,3"/>
            <path d="M 440,180 C 420,230 410,270 400,310" fill="none" stroke="#a0d2db" stroke-width="2" stroke-dasharray="4,3"/>
            
            <!-- 城市标注 -->
            <circle cx="80" cy="125" r="8" fill="#8B4513" stroke="#D4AF37" stroke-width="2"/>
            <text x="95" y="120" fill="#333" font-size="12" font-weight="600">云南镇雄（发源地）</text>
            
            <circle cx="200" cy="135" r="12" fill="#c0392b" stroke="#D4AF37" stroke-width="3"/>
            <text x="215" y="122" fill="#c0392b" font-size="13" font-weight="700">仁怀·茅台镇</text>
            <text x="215" y="138" fill="#999" font-size="10">🏛️ 核心产区 · 356家酒厂</text>
            
            <circle cx="300" cy="160" r="8" fill="#8B4513" stroke="#D4AF37" stroke-width="2"/>
            <text x="312" y="155" fill="#333" font-size="12" font-weight="600">习水</text>
            <text x="312" y="170" fill="#999" font-size="10">🏭 215家酒厂</text>
            
            <circle cx="380" cy="155" r="7" fill="#8B4513" stroke="#D4AF37" stroke-width="2"/>
            <text x="390" y="150" fill="#333" font-size="12" font-weight="600">金沙</text>
            <text x="390" y="165" fill="#999" font-size="10">🌟 180家酒厂</text>
            
            <circle cx="500" cy="185" r="9" fill="#c0392b" stroke="#D4AF37" stroke-width="3"/>
            <text x="512" y="178" fill="#c0392b" font-size="13" font-weight="700">二郎镇·古蔺</text>
            <text x="512" y="194" fill="#999" font-size="10">💎 195家酒厂 · 郎酒大本营</text>
            
            <circle cx="640" cy="190" r="6" fill="#8B4513" stroke="#D4AF37" stroke-width="2"/>
            <text x="650" y="185" fill="#333" font-size="11">遵义</text>
            <text x="650" y="199" fill="#999" font-size="10">🗺️ 大产区 · 850家酒厂</text>
            
            <circle cx="750" cy="210" r="6" fill="#48a9e6" stroke="#7ec8e3" stroke-width="2"/>
            <text x="695" y="225" fill="#48a9e6" font-size="11">合江（入长江口）</text>
            
            <!-- 图例 -->
            <rect x="580" y="280" width="200" height="105" rx="6" fill="white" stroke="#ddd"/>
            <text x="595" y="300" fill="#333" font-size="12" font-weight="600">图例</text>
            <circle cx="598" cy="316" r="6" fill="#c0392b" stroke="#D4AF37" stroke-width="2"/>
            <text x="612" y="321" fill="#666" font-size="11">核心产区</text>
            <circle cx="598" cy="336" r="5" fill="#8B4513" stroke="#D4AF37" stroke-width="1.5"/>
            <text x="612" y="341" fill="#666" font-size="11">重要产区</text>
            <circle cx="598" cy="356" r="4" fill="#48a9e6" stroke="#7ec8e3" stroke-width="1.5"/>
            <text x="612" y="361" fill="#666" font-size="11">河流交汇点</text>
          </svg>
          <p class="map-note">赤水河发源于云南镇雄，流经贵州仁怀、习水、四川古蔺，在合江汇入长江。全长436.5公里，是长江上游唯一未建水坝的一级支流。沿岸分布着超过2000家酱酒企业，贡献了中国90%以上的优质酱酒产能。</p>
        </div>
      </div>

      <!-- 产区列表 -->
      <div class="region-grid">
        <div v-for="area in areas" :key="area.id" class="region-card" @click="goDetail(area.id)">
          <div class="region-top">
            <span class="region-icon">{{ area.icon }}</span>
            <div>
              <h3>{{ area.name }}</h3>
              <p class="region-loc">{{ area.region }}</p>
            </div>
          </div>
          <p class="region-desc">{{ area.description }}</p>
          <div class="region-stats">
            <span>📐 {{ area.area }}km²</span>
            <span>🏭 {{ formatNum(area.winery_count) }}家酒厂</span>
            <span>📊 年产{{ formatNum(area.output) }}吨</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { productionApi } from '@/api'

const router = useRouter()
const loading = ref(true)
const error = ref(null)
const areas = ref([])

const totalRegions = computed(() => areas.value.length)
const totalOutput = computed(() => areas.value.reduce((s,a) => s + (a.output||0), 0))
const totalValue = computed(() => areas.value.reduce((s,a) => s + (a.output_value||0), 0))
const totalWineries = computed(() => areas.value.reduce((s,a) => s + (a.winery_count||0), 0))

const formatNum = (n) => n >= 10000 ? (n/10000).toFixed(1)+'万' : String(n)
const goDetail = (id) => router.push('/production/'+id)

async function fetchData() {
  loading.value = true; error.value = null
  try {
    const res = await productionApi.getList({ page:1, page_size:30 })
    areas.value = res.data.list || []
  } catch(e) { error.value = '加载失败' }
  finally { loading.value = false }
}

onMounted(fetchData)
</script>

<style scoped>
.page-title { font-size: 24px; color: #333; font-weight: 600; margin-bottom: 20px; }
.state-box { text-align: center; padding: 60px 0; color: #999; font-size: 14px; }
.state-box.error { color: #e74c3c; }
.retry-btn { margin-top: 12px; padding: 6px 20px; border-radius: 16px; border:1px solid #8B4513; background:#8B4513; color:#fff; cursor:pointer; font-size:13px; }

/* 概览统计 */
.stats-bar {
  display: flex; gap: 10px; margin-bottom: 20px;
}
.stat-item {
  flex:1; text-align:center; padding:16px 8px;
  background:#fff; border-radius:10px; box-shadow:0 1px 4px rgba(0,0,0,.06);
}
.stat-val { display:block; font-size:22px; font-weight:700; color:#8B4513; margin-bottom:4px; }
.stat-label { font-size:12px; color:#999; }

/* 地图 */
.map-card {
  background:#fff; border-radius:12px; padding:24px; margin-bottom:20px;
  box-shadow:0 1px 4px rgba(0,0,0,.06);
}
.map-card h2 { font-size:18px; color:#8B4513; margin-bottom:16px; }
.map-area { text-align:center; }
.river-map { width:100%; height:auto; max-height:420px; display:block; border-radius:8px; }
.map-note { font-size:13px; color:#999; line-height:1.6; max-width:560px; margin:12px auto 0; text-align:center; }

/* 产区列表 */
.region-grid {
  display:grid; grid-template-columns:repeat(3,1fr); gap:14px;
}
.region-card {
  background:#fff; border-radius:10px; padding:18px;
  box-shadow:0 1px 4px rgba(0,0,0,.06); cursor:pointer;
  transition: transform .2s, box-shadow .2s;
}
.region-card:hover { transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,.1); }
.region-top { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.region-icon { font-size:32px; }
.region-top h3 { font-size:15px; color:#333; margin:0; }
.region-loc { font-size:12px; color:#999; margin:2px 0 0; }
.region-desc { font-size:13px; color:#8B4513; margin:0 0 10px; line-height:1.5; }
.region-stats { display:flex; gap:8px; flex-wrap:wrap; font-size:11px; color:#bbb; }
</style>
