<template>
  <div class="home">
    <div style="background:linear-gradient(135deg, #8B4513 0%, #A0522D 100%); color:white; padding:80px 20px; text-align:center; border-radius:16px; margin-bottom:40px;">
      <h1 style="font-size:42px; margin-bottom:16px;">探索酱酒文化的奥秘</h1>
      <p style="font-size:18px; opacity:0.9;">传承千年酿造工艺，品味酱香独特魅力</p>
    </div>
    
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin-bottom:40px;">
      <div v-for="stat in stats" :key="stat.label" style="background:white; padding:24px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.1); text-align:center;">
        <div style="font-size:32px; font-weight:700; color:#8B4513;">{{ stat.value }}</div>
        <div style="font-size:14px; color:#666;">{{ stat.label }}</div>
      </div>
    </div>
    
    <h2 style="font-size:28px; text-align:center; margin-bottom:32px; color:#333;">快速导航</h2>
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:20px;">
      <router-link to="/knowledge" style="background:white; padding:32px 24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; text-decoration:none; color:inherit;">
        <div style="font-size:48px; margin-bottom:16px;">📚</div>
        <h3 style="font-size:18px; color:#333; margin-bottom:8px;">酱酒知识库</h3>
        <p style="font-size:14px; color:#666;">探索酿造工艺与历史文化</p>
      </router-link>
      <router-link to="/production" style="background:white; padding:32px 24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; text-decoration:none; color:inherit;">
        <div style="font-size:48px; margin-bottom:16px;">🗺️</div>
        <h3 style="font-size:18px; color:#333; margin-bottom:8px;">产区数据</h3>
        <p style="font-size:14px; color:#666;">了解核心产区分布与特点</p>
      </router-link>
      <router-link to="/wineries" style="background:white; padding:32px 24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; text-decoration:none; color:inherit;">
        <div style="font-size:48px; margin-bottom:16px;">🏭</div>
        <h3 style="font-size:18px; color:#333; margin-bottom:8px;">酒厂名录</h3>
        <p style="font-size:14px; color:#666;">发现优质酱酒企业</p>
      </router-link>
      <router-link to="/news" style="background:white; padding:32px 24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; text-decoration:none; color:inherit;">
        <div style="font-size:48px; margin-bottom:16px;">📰</div>
        <h3 style="font-size:18px; color:#333; margin-bottom:8px;">行业资讯</h3>
        <p style="font-size:14px; color:#666;">获取最新行业动态</p>
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
