<template>
  <div class="news-detail-page">
    <div class="container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <router-link to="/news">行业资讯</router-link>
        <span class="separator">/</span>
        <span class="current">{{ news.title }}</span>
      </div>
      
      <div v-if="loading" style="text-align:center; padding:80px 0;">
        <div style="font-size:48px;">⏳</div>
        <p style="color:#999;">加载中...</p>
      </div>

      <div v-else-if="error" style="text-align:center; padding:80px 0;">
        <div style="font-size:48px;">⚠️</div>
        <p style="color:#e74c3c;">{{ error }}</p>
      </div>

      <article v-else class="news-content">
        <header class="news-header">
          <span class="news-tag" :class="news.type">{{ categoryName }}</span>
          <h1 class="news-title">{{ news.title }}</h1>
          <div class="news-meta">
            <span class="meta-item">
              <el-icon><Calendar /></el-icon>
              {{ formatDate(news.publish_time) }}
            </span>
            <span class="meta-item">
              <el-icon><Location /></el-icon>
              {{ news.source }}
            </span>
            <span class="meta-item">
              <el-icon><View /></el-icon>
              {{ news.views || 0 }} 阅读
            </span>
          </div>
        </header>
        
        <div class="news-body" v-html="news.content"></div>
        
        <div class="related-section">
          <h3>相关推荐</h3>
          <div class="related-list">
            <div class="related-item" v-for="item in relatedNews" :key="item.id" @click="goToDetail(item.id)">
              <h4>{{ item.title }}</h4>
              <span>{{ formatDate(item.publish_time) }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Calendar, Location, View } from '@element-plus/icons-vue'
import { newsApi } from '@/api'

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const error = ref(null)
const news = ref({ title: '加载中...', source: '', views: 0, content: '' })
const relatedNews = ref([])

const categoryName = computed(() => {
  const names = { policy: '政策动态', trend: '行业趋势', company: '企业新闻', event: '展会活动' }
  return names[news.value.type] || '资讯'
})

const formatDate = (d) => d ? d.slice(0, 10) : ''

const goToDetail = (id) => router.push(`/news/${id}`)

onMounted(async () => {
  try {
    const res = await newsApi.getDetail(route.params.id)
    if (res.code === 200 && res.data) {
      news.value = res.data
    }
    // Fetch related news
    const listRes = await newsApi.getList({ page: 1, page_size: 4 })
    if (listRes.code === 200) {
      relatedNews.value = (listRes.data.list || []).filter(n => n.id !== route.params.id).slice(0, 3)
    }
  } catch (e) {
    error.value = '加载失败，请检查网络连接'
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.news-detail-page {
  padding: 20px 0 40px;
}
.breadcrumb {
  display: flex; align-items: center; gap: 8px; font-size: 14px; color: #999; margin-bottom: 24px;
  a { color: #666; text-decoration: none; &:hover { color: #8B4513; } }
  .current { color: #333; font-weight: 500; }
}
.news-content {
  background: white; border-radius: 12px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  .news-header {
    margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid #eee;
    .news-tag { display: inline-block; padding: 6px 16px; background: rgba(76,175,80,0.1); color: #4CAF50; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 16px; }
    .news-title { font-size: 28px; font-weight: 700; color: #333; line-height: 1.4; margin-bottom: 16px; }
    .news-meta { display: flex; align-items: center; gap: 20px; font-size: 14px; color: #999; flex-wrap: wrap; }
    .meta-item { display: flex; align-items: center; gap: 4px; }
  }
  .news-body { font-size: 16px; line-height: 2; color: #333; h3 { font-size: 20px; font-weight: 600; color: #8B4513; margin: 32px 0 16px; } p { margin-bottom: 16px; } }
  .related-section { margin-top: 40px; padding-top: 32px; border-top: 1px solid #eee;
    h3 { font-size: 18px; font-weight: 600; color: #333; margin-bottom: 20px; }
    .related-list { display: flex; flex-direction: column; gap: 12px; }
    .related-item { display: flex; align-items: center; justify-content: space-between; padding: 16px; background: #FAF8F5; border-radius: 8px; cursor: pointer; transition: all 0.3s;
      &:hover { background: rgba(139,69,19,0.05); }
      h4 { font-size: 16px; font-weight: 500; color: #333; flex: 1; margin: 0; }
      span { font-size: 13px; color: #999; white-space: nowrap; margin-left: 16px; }
    }
  }
}
</style>
