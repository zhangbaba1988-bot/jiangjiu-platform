<template>
  <header class="app-header">
    <div class="container">
      <div class="header-content">
        <div class="logo" @click="goHome">
          <div class="logo-text">
            <h1>酱酒研学平台</h1>
            <span>传承千年酱香文化</span>
          </div>
        </div>
        <nav class="desktop-nav">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: $route.path === item.path || $route.path.startsWith(item.path + '/') }"
          >
            {{ item.name }}
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const navItems = [
  { path: '/', name: '首页' },
  { path: '/knowledge', name: '知识库' },
  { path: '/production', name: '产区数据' },
  { path: '/wineries', name: '酒厂名录' },
  { path: '/news', name: '行业资讯' },
  { path: '/profile', name: '个人中心' }
]

const goHome = () => {
  router.push('/')
}
</script>

<style lang="scss" scoped>
.app-header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;

  h1 {
    font-size: 20px;
    color: $primary-color;
    margin: 0;
  }

  span {
    font-size: 12px;
    color: $text-light;
    display: block;
  }
}

.desktop-nav {
  display: flex;
  gap: 32px;

  @include respond-to(mobile) {
    display: none;
  }

  .nav-item {
    color: $text-color;
    font-size: 15px;
    font-weight: 500;
    transition: color 0.3s;
    text-decoration: none;

    &:hover,
    &.active {
      color: $primary-color;
    }
  }
}
</style>
