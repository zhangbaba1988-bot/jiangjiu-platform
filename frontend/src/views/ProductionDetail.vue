<template>
  <div class="production-detail">
    <el-page-header @back="goBack" :content="production.name">
      <template #extra>
        <el-tag type="success">{{ production.region }}</el-tag>
      </template>
    </el-page-header>

    <div class="detail-content" v-loading="loading">
      <!-- 产区概览 -->
      <el-card class="overview-card">
        <template #header>
          <div class="card-header">
            <span>产区概览</span>
          </div>
        </template>
        <div class="overview-grid">
          <div class="overview-item">
            <div class="label">酒厂数量</div>
            <div class="value">{{ production.winery_count || 0 }} 家</div>
          </div>
          <div class="overview-item">
            <div class="label">年产量</div>
            <div class="value">{{ production.output ? (production.output/1000).toFixed(1) : 0 }} 万吨</div>
          </div>
          <div class="overview-item">
            <div class="label">年产值</div>
            <div class="value">{{ production.output_value || 0 }} 亿元</div>
          </div>
          <div class="overview-item">
            <div class="label">核心品牌</div>
            <div class="value">{{ production.brands?.length || 0 }} 个</div>
          </div>
        </div>
      </el-card>

      <!-- 产区介绍 -->
      <el-card class="intro-card">
        <template #header>
          <div class="card-header">
            <span>产区介绍</span>
          </div>
        </template>
        <div class="intro-content" v-html="production.description"></div>
      </el-card>

      <!-- 地理环境 -->
      <el-card class="env-card" v-if="production.environment">
        <template #header>
          <div class="card-header">
            <span>地理环境</span>
          </div>
        </template>
        <div class="env-content" v-html="production.environment"></div>
      </el-card>

      <!-- 代表酒厂 -->
      <el-card class="wineries-card" v-if="production.wineries?.length > 0">
        <template #header>
          <div class="card-header">
            <span>代表酒厂</span>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :xs="12" :sm="8" :md="6" v-for="winery in production.wineries" :key="winery.id">
            <div class="winery-item" @click="goWineryDetail(winery.id)">
              <el-image :src="winery.logo" class="winery-logo" fit="cover">
                <template #error>
                  <div class="image-slot">
                    <el-icon size="40"><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
              <div class="winery-name">{{ winery.name }}</div>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 数据统计 -->
      <el-card class="stats-card">
        <template #header>
          <div class="card-header">
            <span>发展数据</span>
          </div>
        </template>
        <div ref="chartRef" class="chart-container"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { productionApi } from '@/api'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const production = ref({})
const chartRef = ref(null)

const id = route.params.id

const fetchDetail = async () => {
  loading.value = true
  try {
    const res = await productionApi.getDetail(id)
    if (res.code === 200) {
      production.value = res.data
    }
  } catch (e) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

const goWineryDetail = (wineryId) => {
  router.push(`/wineries/${wineryId}`)
}

const initChart = () => {
  if (!chartRef.value) return
  
  const chart = echarts.init(chartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['产量(千升)', '产值(亿元)']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['2019', '2020', '2021', '2022', '2023', '2024', '2025']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '产量(千升)',
        type: 'line',
        stack: 'Total',
        data: [150, 180, 220, 260, 320, 350, 380],
        smooth: true,
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: '产值(亿元)',
        type: 'line',
        stack: 'Total',
        data: [80, 100, 140, 180, 230, 280, 320],
        smooth: true,
        itemStyle: {
          color: '#67c23a'
        }
      }
    ]
  }
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

onMounted(() => {
  fetchDetail()
  setTimeout(initChart, 500)
})
</script>

<style scoped lang="scss">
.production-detail {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.detail-content {
  margin-top: 20px;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.overview-card {
  margin-bottom: 20px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.overview-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.overview-item .label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.overview-item .value {
  font-size: 24px;
  font-weight: 600;
}

.intro-card,
.env-card,
.wineries-card,
.stats-card {
  margin-bottom: 20px;
}

.intro-content,
.env-content {
  line-height: 1.8;
  color: #606266;
  
  :deep(p) {
    margin-bottom: 12px;
  }
  
  :deep(h3) {
    margin: 16px 0 8px;
    color: #303133;
  }
}

.winery-item {
  text-align: center;
  cursor: pointer;
  padding: 16px;
  border-radius: 8px;
  transition: all 0.3s;
  
  &:hover {
    background: #f5f7fa;
    transform: translateY(-2px);
  }
}

.winery-logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin: 0 auto 12px;
  border: 2px solid #e4e7ed;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  background: #f5f7fa;
  color: #909399;
  border-radius: 50%;
}

.winery-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.chart-container {
  height: 350px;
}
</style>
