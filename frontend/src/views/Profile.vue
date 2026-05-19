<template>
  <div class="profile">
    <h1 style="font-size:32px; color:#333; margin-bottom:32px;">个人中心</h1>
    
    <div v-if="loading" style="text-align:center; padding:80px 0;">
      <div style="font-size:48px;">⏳</div>
      <p style="color:#999;">加载中...</p>
    </div>

    <template v-else>
      <div style="background:white; padding:32px; border-radius:12px; box-shadow:0 2px 16px rgba(0,0,0,0.1); margin-bottom:30px; display:flex; align-items:center; gap:24px;">
        <div style="width:100px; height:100px; background:linear-gradient(135deg, #8B4513 0%, #D4AF37 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:48px; color:white;">👤</div>
        <div>
          <h2 style="font-size:24px; color:#333; margin-bottom:8px;">{{ profile.nickname || '酱酒爱好者' }}</h2>
          <p style="font-size:14px; color:#666;">ID：{{ profile.id || '--' }}</p>
        </div>
      </div>
      
      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:30px;">
        <div style="background:white; padding:24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;">
          <div style="font-size:36px; font-weight:700; color:#8B4513;">{{ profile.history_count || 0 }}</div>
          <div style="font-size:14px; color:#666;">浏览历史</div>
        </div>
        <div style="background:white; padding:24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;">
          <div style="font-size:36px; font-weight:700; color:#D4AF37;">{{ profile.favorite_count || 0 }}</div>
          <div style="font-size:14px; color:#666;">收藏文章</div>
        </div>
        <div style="background:white; padding:24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;">
          <div style="font-size:36px; font-weight:700; color:#666;">--</div>
          <div style="font-size:14px; color:#666;">浏览酒厂</div>
        </div>
      </div>
      
      <div style="background:white; padding:24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <h3 style="font-size:20px; color:#333; margin-bottom:20px;">快捷功能</h3>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px;">
          <router-link v-for="item in menuItems" :key="item.name" :to="item.to || '#'"
            style="text-align:center; padding:20px; border-radius:8px; background:#FAF8F5; cursor:pointer; text-decoration:none; color:inherit;">
            <div style="font-size:32px; margin-bottom:8px;">{{ item.icon }}</div>
            <div style="font-size:14px; color:#333;">{{ item.name }}</div>
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { userApi } from '@/api'

const loading = ref(true)
const profile = ref({})

const menuItems = ref([
  { name: '我的收藏', icon: '⭐' },
  { name: '浏览历史', icon: '📋' },
  { name: '设置', icon: '⚙️' },
  { name: '帮助中心', icon: '❓' }
])

onMounted(async () => {
  try {
    const res = await userApi.getProfile()
    if (res.code === 200 && res.data) {
      profile.value = res.data
    }
  } catch {} finally {
    loading.value = false
  }
})
</script>
