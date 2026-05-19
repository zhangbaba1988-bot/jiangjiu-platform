<template>
  <div class="search-page">
    <div class="container">
      <!-- 搜索框 -->
      <section class="search-section">
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索文章、酒厂、资讯..."
            :prefix-icon="Search"
            size="large"
            clearable
            @keyup.enter="doSearch"
          >
            <template #append>
              <el-button type="primary" @click="doSearch">搜索</el-button>
            </template>
          </el-input>
        </div>
      </section>
      
      <!-- 搜索历史 -->
      <section class="history-section" v-if="searchHistory.length > 0 && !showResults">
        <div class="section-header">
          <h3 class="section-title">搜索历史</h3>
          <button class="clear-btn" @click="clearHistory">清空</button>
        </div>
        <div class="history-tags">
          <span 
            class="history-tag" 
            v-for="(item, index) in searchHistory" 
            :key="index"
            @click="searchByHistory(item)"
          >
            {{ item }}
          </span>
        </div>
      </section>
      
      <!-- 热门搜索 -->
      <section class="hot-section" v-if="!showResults">
        <div class="section-header">
          <h3 class="section-title">热门搜索</h3>
        </div>
        <div class="hot-tags">
          <span 
            class="hot-tag" 
            v-for="(item, index) in hotSearches" 
            :key="index"
            @click="searchByHistory(item)"
          >
            <span class="hot-rank" :class="{ top: index < 3 }">{{ index + 1 }}</span>
            {{ item }}
          </span>
        </div>
      </section>
      
      <!-- 搜索结果 -->
      <section class="results-section" v-if="showResults">
        <div class="results-header">
          <h3 class="results-title">
            搜索结果：<span>"{{ searchKeyword }}"</span>
          </h3>
          <span class="results-count">共找到 {{ totalResults }} 条结果</span>
        </div>
        
        <!-- 分类标签 -->
        <div class="result-tabs">
          <button 
            v-for="tab in resultTabs" 
            :key="tab.id"
            class="result-tab"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.name }} ({{ getTabCount(tab.id) }})
          </button>
        </div>
        
        <!-- 知识库结果 -->
        <div v-if="activeTab === 'all' || activeTab === 'knowledge'" class="result-category">
          <div 
            class="result-item" 
            v-for="item in knowledgeResults" 
            :key="item.id"
            @click="goToDetail(item.id, 'knowledge')"
          >
            <div class="result-type">知识库</div>
            <div class="result-content">
              <h4 class="result-title" v-html="highlightKeyword(item.title)"></h4>
              <p class="result-desc" v-html="highlightKeyword(item.summary)"></p>
              <div class="result-meta">
                <span>{{ item.category }}</span>
                <span>{{ item.date }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 酒厂结果 -->
        <div v-if="activeTab === 'all' || activeTab === 'wineries'" class="result-category">
          <div 
            class="result-item winery" 
            v-for="item in wineryResults" 
            :key="item.id"
            @click="goToDetail(item.id, 'wineries')"
          >
            <div class="result-type winery">酒厂</div>
            <div class="result-content">
              <h4 class="result-title" v-html="highlightKeyword(item.name)"></h4>
              <p class="result-desc" v-html="highlightKeyword(item.description)"></p>
              <div class="result-meta">
                <span>{{ item.area }}</span>
                <span>成立于 {{ item.foundedYear }}年</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 资讯结果 -->
        <div v-if="activeTab === 'all' || activeTab === 'news'" class="result-category">
          <div 
            class="result-item" 
            v-for="item in newsResults" 
            :key="item.id"
            @click="goToDetail(item.id, 'news')"
          >
            <div class="result-type news">资讯</div>
            <div class="result-content">
              <h4 class="result-title" v-html="highlightKeyword(item.title)"></h4>
              <p class="result-desc" v-html="highlightKeyword(item.summary)"></p>
              <div class="result-meta">
                <span>{{ item.source }}</span>
                <span>{{ item.date }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="totalResults === 0" class="empty-state">
          <el-icon :size="64" color="#D4AF37"><Search /></el-icon>
          <p>未找到相关内容</p>
          <p class="empty-tip">试试其他关键词吧</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import { searchApi } from '@/api'

const router = useRouter()
const searchKeyword = ref('')
const showResults = ref(false)
const activeTab = ref('all')
const searching = ref(false)

const searchHistory = ref(['12987工艺', '茅台镇', '酱酒品鉴', '赤水河'])

const hotSearches = ref([])

const resultTabs = ref([
  { id: 'all', name: '全部' },
  { id: 'knowledge', name: '知识库' },
  { id: 'wineries', name: '酒厂' },
  { id: 'news', name: '资讯' }
])

const knowledgeResults = ref([])
const wineryResults = ref([])
const newsResults = ref([])

const totalResults = computed(() => {
  return knowledgeResults.value.length + wineryResults.value.length + newsResults.value.length
})

const getTabCount = (tabId) => {
  if (tabId === 'all') return totalResults.value
  if (tabId === 'knowledge') return knowledgeResults.value.length
  if (tabId === 'wineries') return wineryResults.value.length
  if (tabId === 'news') return newsResults.value.length
  return 0
}

const highlightKeyword = (text) => {
  if (!searchKeyword.value || !text) return text
  const escaped = searchKeyword.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${escaped})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

const doSearch = async () => {
  if (!searchKeyword.value.trim()) return
  
  if (!searchHistory.value.includes(searchKeyword.value)) {
    searchHistory.value.unshift(searchKeyword.value)
    if (searchHistory.value.length > 10) {
      searchHistory.value.pop()
    }
  }
  
  searching.value = true
  showResults.value = true
  
  try {
    const res = await searchApi.search(searchKeyword.value)
    if (res.code === 200 && res.data) {
      knowledgeResults.value = (res.data.knowledge || []).map(k => ({ ...k, date: k.created_at?.slice(0,10) }))
      wineryResults.value = (res.data.wineries || []).map(w => ({ ...w, area: w.production }))
      newsResults.value = (res.data.news || []).map(n => ({ ...n, date: n.publish_time?.slice(0,10) }))
    }
  } catch (e) {
    knowledgeResults.value = []
    wineryResults.value = []
    newsResults.value = []
  } finally {
    searching.value = false
  }
}

const searchByHistory = (keyword) => {
  searchKeyword.value = keyword
  doSearch()
}

const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空搜索历史吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    searchHistory.value = []
  } catch {}
}

const goToDetail = (id, type) => {
  router.push(`/${type}/${id}`)
}

// Fetch hot searches on mount
onMounted(async () => {
  try {
    const res = await searchApi.getHotSearches()
    if (res.code === 200 && res.data) {
      hotSearches.value = (res.data || []).map(h => h.keyword)
    }
  } catch {}
})
</script>

<style lang="scss" scoped>
.search-page {
  min-height: calc(100vh - 70px);
  padding: $spacing-xl 0;
}

.search-section {
  margin-bottom: $spacing-xl;
  
  .search-box {
    max-width: 600px;
    margin: 0 auto;
    
    :deep(.el-input__wrapper) {
      border-radius: 50px;
      padding-left: $spacing-lg;
      box-shadow: $shadow-md;
    }
    
    :deep(.el-input-group__append) {
      border-radius: 0 50px 50px 0;
      
      .el-button {
        border-radius: 0 50px 50px 0;
        padding: 0 $spacing-xl;
      }
    }
  }
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-md;
  
  .section-title {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $text-color;
  }
  
  .clear-btn {
    font-size: $font-size-sm;
    color: $text-muted;
    background: none;
    border: none;
    cursor: pointer;
    
    &:hover {
      color: $primary-color;
    }
  }
}

.history-section,
.hot-section {
  margin-bottom: $spacing-xl;
}

.history-tags,
.hot-tags {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-md;
}

.history-tag {
  padding: 8px 20px;
  background: $bg-color;
  border-radius: 20px;
  font-size: $font-size-sm;
  color: $text-color;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba($primary-color, 0.1);
    color: $primary-color;
  }
}

.hot-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border-radius: 24px;
  font-size: $font-size-sm;
  color: $text-color;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: $shadow-sm;
  
  &:hover {
    box-shadow: $shadow-md;
  }
  
  .hot-rank {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $text-muted;
    color: white;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 600;
    
    &.top {
      background: $gradient-gold;
      color: $primary-color;
    }
  }
}

.results-section {
  .results-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: $spacing-lg;
    flex-wrap: wrap;
    gap: $spacing-md;
  }
  
  .results-title {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $text-color;
    
    span {
      color: $primary-color;
    }
  }
  
  .results-count {
    font-size: $font-size-sm;
    color: $text-muted;
  }
}

.result-tabs {
  display: flex;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
  padding-bottom: $spacing-md;
  border-bottom: 1px solid $border-color;
  overflow-x: auto;
}

.result-tab {
  padding: $spacing-sm $spacing-lg;
  border: none;
  background: none;
  font-size: $font-size-md;
  color: $text-light;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: $radius-md;
  white-space: nowrap;
  
  &:hover {
    background: rgba($primary-color, 0.05);
  }
  
  &.active {
    background: $gradient-primary;
    color: white;
  }
}

.result-category {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.result-item {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-lg;
  background: white;
  border-radius: $radius-lg;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: $shadow-sm;
  
  &:hover {
    box-shadow: $shadow-md;
    transform: translateX(4px);
  }
  
  &.winery .result-type {
    background: rgba(156, 39, 176, 0.1);
    color: #9C27B0;
  }
  
  &.news .result-type {
    background: rgba(255, 152, 0, 0.1);
    color: #FF9800;
  }
  
  .result-type {
    padding: 4px 10px;
    background: rgba($primary-color, 0.1);
    color: $primary-color;
    border-radius: 12px;
    font-size: $font-size-xs;
    font-weight: 600;
    height: fit-content;
    white-space: nowrap;
  }
  
  .result-content {
    flex: 1;
    
    .result-title {
      font-size: $font-size-md;
      font-weight: 600;
      color: $text-color;
      margin-bottom: $spacing-sm;
      
      mark {
        background: rgba($secondary-color, 0.3);
        color: $primary-color;
        padding: 0 2px;
      }
    }
    
    .result-desc {
      font-size: $font-size-sm;
      color: $text-light;
      line-height: 1.6;
      margin-bottom: $spacing-sm;
      
      mark {
        background: rgba($secondary-color, 0.3);
        color: $primary-color;
        padding: 0 2px;
      }
    }
    
    .result-meta {
      display: flex;
      gap: $spacing-lg;
      font-size: $font-size-xs;
      color: $text-muted;
    }
  }
}

.empty-state {
  text-align: center;
  padding: $spacing-xxl 0;
  color: $text-muted;
  
  p {
    margin-top: $spacing-md;
    font-size: $font-size-md;
    
    &.empty-tip {
      font-size: $font-size-sm;
      margin-top: $spacing-sm;
    }
  }
}
</style>
