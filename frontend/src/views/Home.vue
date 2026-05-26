<template>
  <div class="home-page">
    <!-- ===== Hero 区域 ===== -->
    <section class="hero-section">
      <!-- 装饰纹样背景 -->
      <div class="hero-pattern"></div>
      <div class="hero-content">
        <div class="hero-text">
          <p class="hero-kicker">传承千年 · 品味酱香</p>
          <h1 class="hero-title">{{ hero.title }}</h1>
          <p class="hero-desc">{{ hero.description }}</p>
          <div class="hero-actions">
            <router-link :to="hero.ctaLink || '/knowledge'" class="btn-primary">
              <el-icon><Reading /></el-icon>
              <span>{{ hero.ctaText }}</span>
            </router-link>
            <router-link to="/forum" class="btn-outline">
              <el-icon><ChatDotRound /></el-icon>
              <span>进入论坛</span>
            </router-link>
          </div>
        </div>

        <!-- 站点动态面板 -->
        <div class="hero-panel">
          <div class="panel-header">
            <span class="panel-dot"></span>
            <span class="panel-label">站点数据更新中</span>
          </div>
          <div class="panel-stats">
            <div class="panel-stat-item" v-for="s in stats.slice(0, 3)" :key="s.label">
              <strong>{{ s.value }}</strong>
              <span>{{ s.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== 导航入口区域 ===== -->
    <section class="nav-section">
      <div class="section-header">
        <h2 class="section-title">探索酱酒世界</h2>
        <p class="section-subtitle">汇聚行业资源，打造酱酒知识中枢，一站式浏览知识、产区、酒厂与行业动态</p>
      </div>
      <div class="nav-grid">
        <router-link v-for="(item, i) in navCards" :key="item.path" :to="item.path" class="nav-card" :style="{ animationDelay: i * 0.08 + 's' }">
          <div class="nav-card-icon" :class="'icon-color-' + i">
            <el-icon :size="32"><component :is="item.icon" /></el-icon>
          </div>
          <div class="nav-card-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
            <span class="nav-card-tag">{{ item.tag }}</span>
          </div>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, shallowRef } from 'vue'
import { MapLocation, OfficeBuilding, ChatDotRound, Phone, DataAnalysis, Collection, Document, TrendCharts } from '@element-plus/icons-vue'
import service from '@/api'
import { loadSiteContent } from '@/utils/siteContent'

const hero = ref(loadSiteContent().hero)

const statIcons = [
  shallowRef(MapLocation),
  shallowRef(OfficeBuilding),
  shallowRef(Document),
  shallowRef(TrendCharts)
]

const stats = ref([
  { value: '12', label: '核心产区' },
  { value: '500+', label: '酒厂数据库' },
  { value: '1000+', label: '知识文章' },
  { value: '800+', label: '行业资讯' }
])

const navCards = [
  { path: '/knowledge',  icon: shallowRef(Collection),   title: '酱酒知识库', tag: '酿造·品鉴·文化',   desc: '探索酿造工艺、历史脉络与品鉴知识，建立系统的酱酒认知体系。' },
  { path: '/production', icon: shallowRef(TrendCharts), title: '产区数据',     tag: '分布·产能·特点',   desc: '查看核心产区地理分布、产能数据与区域特色分析。' },
  { path: '/wineries',   icon: shallowRef(OfficeBuilding), title: '酒厂名录',   tag: '品牌·实力·传承',   desc: '快速浏览知名酒厂详情、品牌故事与生产实力。' },
  { path: '/news',       icon: shallowRef(Document),    title: '行业资讯',     tag: '政策·市场·动态',   desc: '获取最新行业政策、市场行情与企业动态。' },
  { path: '/forum',      icon: shallowRef(ChatDotRound), title: '论坛板块',    tag: '交流·分享·互助',   desc: '参与话题讨论，与酱酒爱好者社群一起交流经验。' },
  { path: '/contact',    icon: shallowRef(Phone),       title: '联系我们',       tag: '合作·反馈·对接',   desc: '商务合作、内容对接与用户反馈的统一入口通道。' }
]

onMounted(async () => {
  hero.value = loadSiteContent().hero
  try {
    const res = await service.get('/dashboard')
    if (res.code === 200 && res.data?.statistics) {
      const s = res.data.statistics
      stats.value = [
        { value: (s.production_count || '6') + '个', label: '核心产区' },
        { value: (s.wineries_count   || '6') + '家', label: '酒厂数据库' },
        { value: (s.knowledge_count  || '15') + '篇', label: '知识文章' },
        { value: (s.news_count       || '10') + '条', label: '行业资讯' }
      ]
    }
  } catch {}
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

// ==================== 通用 ====================
.home-page {
  display: flex;
  flex-direction: column;
  gap: 56px;
  padding-bottom: 16px;
}

.section-header {
  text-align: center;
  margin-bottom: 28px;
}

.section-title {
  font-size: 30px;
  font-weight: 700;
  color: #2f241d;
  letter-spacing: 0.02em;
}

.section-subtitle {
  margin-top: 8px;
  color: #8c7a6b;
  font-size: 15px;
}

// ==================== Hero ====================
.hero-section {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  background: linear-gradient(135deg, #5c2d15 0%, #8B4513 40%, #A0522D 70%, #6B3410 100%);
  min-height: 380px;
}

// 装饰纹样 — CSS 伪元素实现传统云纹/水纹
.hero-pattern {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.08;

  &::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -40px;
    width: 420px;
    height: 420px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.3);
  }

  &::after {
    content: '';
    position: absolute;
    top: -20px;
    right: 0;
    width: 380px;
    height: 380px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.15);
  }

  // 云纹圆点装饰
  background-image:
    radial-gradient(circle at 85% 20%, rgba(212,175,55,0.3) 2px, transparent 2px),
    radial-gradient(circle at 78% 35%, rgba(212,175,55,0.25) 3px, transparent 3px),
    radial-gradient(circle at 90% 50%, rgba(212,175,55,0.2) 4px, transparent 4px),
    radial-gradient(circle at 82% 65%, rgba(212,175,55,0.25) 2px, transparent 2px),
    radial-gradient(circle at 15% 85%, rgba(212,175,55,0.15) 4px, transparent 4px),
    radial-gradient(circle at 20% 75%, rgba(212,175,55,0.2) 3px, transparent 3px),
    radial-gradient(circle at 30% 50%, rgba(212,175,55,0.12) 5px, transparent 5px);

  // 斜线装饰
  & {
    background-image:
      repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(212,175,55,0.04) 35px, rgba(212,175,55,0.04) 36px),
      radial-gradient(circle at 85% 20%, rgba(212,175,55,0.3) 2px, transparent 2px),
      radial-gradient(circle at 78% 35%, rgba(212,175,55,0.25) 3px, transparent 3px),
      radial-gradient(circle at 90% 50%, rgba(212,175,55,0.2) 4px, transparent 4px);
  }
}

.hero-content {
  position: relative;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 32px;
  align-items: stretch;
  padding: 48px 44px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #fff;
}

.hero-kicker {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: $secondary-color;
  margin-bottom: 12px;
  opacity: 0.9;
}

.hero-title {
  font-size: 40px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 16px;
  letter-spacing: 0.03em;
}

.hero-desc {
  font-size: 17px;
  line-height: 1.8;
  max-width: 600px;
  opacity: 0.9;
  margin-bottom: 28px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 13px 26px;
  background: $secondary-color;
  color: #4a2508;
  border-radius: 999px;
  font-weight: 700;
  font-size: 15px;
  text-decoration: none;
  transition: all 0.25s;
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.35);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(212, 175, 55, 0.5);
  }
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 13px 26px;
  background: rgba(255,255,255,0.1);
  color: #fff;
  border: 1.5px solid rgba(255,255,255,0.25);
  border-radius: 999px;
  font-weight: 600;
  font-size: 15px;
  text-decoration: none;
  transition: all 0.25s;
  backdrop-filter: blur(4px);

  &:hover {
    background: rgba(255,255,255,0.18);
    border-color: rgba(255,255,255,0.45);
  }
}

// 右侧面板
.hero-panel {
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 20px;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.panel-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 8px #4ade80;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.panel-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.7);
}

.panel-body {
  h3 {
    font-size: 20px;
    color: #fff;
    font-weight: 700;
    margin-bottom: 8px;
  }
  p {
    color: rgba(255,255,255,0.75);
    font-size: 14px;
    line-height: 1.7;
  }
}

.panel-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 20px;
}

.panel-stat-item {
  background: rgba(255,255,255,0.1);
  border-radius: 14px;
  padding: 14px 8px;
  text-align: center;
  transition: background 0.25s;

  &:hover {
    background: rgba(255,255,255,0.2);
  }

  strong {
    display: block;
    font-size: 20px;
    font-weight: 800;
    color: $secondary-color;
    margin-bottom: 4px;
  }
  span {
    font-size: 11px;
    color: rgba(255,255,255,0.7);
  }
}

// ==================== 统计区域 ====================
.stats-section {
  padding: 0 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.stat-card {
  background: #fff;
  border-radius: 20px;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  box-shadow: 0 4px 24px rgba(139, 69, 19, 0.07);
  transition: all 0.35s;
  animation: fadeInUp 0.6s ease-out both;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    opacity: 0;
    transition: opacity 0.35s;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(139, 69, 19, 0.12);

    &::before { opacity: 1; }
  }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.stat-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-0 { background: #fef3e2; color: #d97706; }
.stat-icon-1 { background: #e8f0fe; color: #2563eb; }
.stat-icon-2 { background: #f0fdf4; color: #16a34a; }
.stat-icon-3 { background: #fdf2f8; color: #db2777; }

.stat-card:nth-child(1)::before { background: linear-gradient(90deg, #d97706, #f59e0b); }
.stat-card:nth-child(2)::before { background: linear-gradient(90deg, #2563eb, #3b82f6); }
.stat-card:nth-child(3)::before { background: linear-gradient(90deg, #16a34a, #22c55e); }
.stat-card:nth-child(4)::before { background: linear-gradient(90deg, #db2777, #ec4899); }

.stat-value {
  font-size: 34px;
  font-weight: 800;
  color: #2f241d;
  line-height: 1.1;
}

.stat-label {
  font-size: 14px;
  color: #8c7a6b;
  font-weight: 500;
}

// ==================== 导航区域 ====================
.nav-section {
  padding: 0 4px;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.nav-card {
  background: #fff;
  border-radius: 20px;
  padding: 28px 24px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 4px 24px rgba(139, 69, 19, 0.06);
  transition: all 0.35s;
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out both;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: $primary-color;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.35s;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(139, 69, 19, 0.13);

    &::after { transform: scaleX(1); }

    .nav-card-icon {
      transform: scale(1.08);
    }
  }
}

.nav-card-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  transition: transform 0.35s;
}

// 每个卡片不同的微妙配色
.icon-color-0 { background: #fef7ed; color: #d97706; }
.icon-color-1 { background: #eff6ff; color: #2563eb; }
.icon-color-2 { background: #f5f3ff; color: #7c3aed; }
.icon-color-3 { background: #fdf2f8; color: #db2777; }
.icon-color-4 { background: #ecfdf5; color: #059669; }
.icon-color-5 { background: #fff7ed; color: #ea580c; }

.nav-card-content {
  h3 {
    font-size: 18px;
    font-weight: 700;
    color: #2f241d;
    margin-bottom: 6px;
  }

  p {
    font-size: 14px;
    color: #8c7a6b;
    line-height: 1.65;
    margin-bottom: 12px;
  }
}

.nav-card-tag {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  color: $primary-color;
  background: #fef7ed;
  padding: 3px 10px;
  border-radius: 999px;
  letter-spacing: 0.02em;
}

// ==================== 响应式 ====================
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    padding: 36px 28px;
  }

  .hero-title { font-size: 32px; }
}

@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .home-page { gap: 36px; }

  .hero-section {
    border-radius: 16px;
  }

  .hero-content {
    padding: 28px 18px;
  }

  .hero-title {
    font-size: 26px;
  }

  .hero-desc {
    font-size: 15px;
  }

  .hero-panel {
    padding: 20px 16px;
  }

  .section-title {
    font-size: 24px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    padding: 20px 14px;
  }

  .stat-value {
    font-size: 26px;
  }

  .nav-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .nav-card {
    padding: 20px 16px;
  }
}

@media (max-width: 480px) {
  .nav-grid {
    grid-template-columns: 1fr;
  }

  .panel-stats {
    grid-template-columns: 1fr;
  }

  .hero-actions {
    flex-direction: column;
  }
}
</style>