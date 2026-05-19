<template>
  <div class="home">
    <div class="hero">
      <h1 class="hero-title">探索酱酒文化的奥秘</h1>
      <p class="hero-desc">传承千年酿造工艺，品味酱香独特魅力</p>
    </div>

    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>

    <h2 class="section-title">快速导航</h2>
    <div class="nav-grid">
      <router-link to="/knowledge" class="nav-card">
        <div class="nav-icon">📚</div>
        <h3 class="nav-name">酱酒知识库</h3>
        <p class="nav-desc">探索酿造工艺与历史文化</p>
      </router-link>
      <router-link to="/production" class="nav-card">
        <div class="nav-icon">🗺️</div>
        <h3 class="nav-name">产区数据</h3>
        <p class="nav-desc">了解核心产区分布与特点</p>
      </router-link>
      <router-link to="/wineries" class="nav-card">
        <div class="nav-icon">🏭</div>
        <h3 class="nav-name">酒厂名录</h3>
        <p class="nav-desc">发现优质酱酒企业</p>
      </router-link>
      <router-link to="/news" class="nav-card">
        <div class="nav-icon">📰</div>
        <h3 class="nav-name">行业资讯</h3>
        <p class="nav-desc">获取最新行业动态</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import service from '@/api'

const stats = ref([
  { value: '12987', label: '传统酿造工艺' },
  { value: '500+', label: '酒厂数据库' },
  { value: '12', label: '核心产区' },
  { value: '1000+', label: '知识文章' }
])

onMounted(async () => {
  try {
    const res = await service.get('/dashboard')
    if (res.code === 200 && res.data && res.data.statistics) {
      const s = res.data.statistics
      stats.value = [
        { value: s.production_count ? s.production_count + '个' : '6', label: '核心产区' },
        { value: s.wineries_count ? s.wineries_count + '家' : '6', label: '酒厂数据库' },
        { value: s.knowledge_count ? s.knowledge_count + '篇' : '15', label: '知识文章' },
        { value: s.news_count ? s.news_count + '条' : '10', label: '行业资讯' }
      ]
    }
  } catch {}
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
  border-radius: 16px;
  margin-bottom: 40px;
}

.hero-title {
  font-size: 42px;
  margin-bottom: 16px;
}

.hero-desc {
  font-size: 18px;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #8B4513;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.section-title {
  font-size: 28px;
  text-align: center;
  margin-bottom: 32px;
  color: #333;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.nav-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.nav-card:active { transform: scale(0.97); }

.nav-icon { font-size: 48px; margin-bottom: 16px; }
.nav-name { font-size: 18px; color: #333; margin-bottom: 8px; }
.nav-desc { font-size: 14px; color: #666; }

/* ===== 移动端 ===== */
@media (max-width: 767px) {
  .hero { padding: 40px 16px; margin-bottom: 20px; border-radius: 12px; }
  .hero-title { font-size: 24px; }
  .hero-desc { font-size: 14px; }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 24px;
  }
  .stat-card { padding: 16px; }
  .stat-value { font-size: 24px; }

  .section-title { font-size: 20px; margin-bottom: 20px; }

  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  .nav-card { padding: 20px 12px; }
  .nav-icon { font-size: 36px; margin-bottom: 10px; }
  .nav-name { font-size: 15px; }
  .nav-desc { font-size: 12px; }
}
</style>
