<template>
  <div id="app">
    <header class="app-header">
      <div class="header-inner">
        <h1 class="logo" @click="$router.push('/')">🍶 酱酒研学平台</h1>
        <button class="menu-toggle" @click="menuOpen = !menuOpen">
          <span class="menu-icon">{{ menuOpen ? '✕' : '☰' }}</span>
        </button>
        <nav class="nav-links" :class="{ mobile: true, open: menuOpen }">
          <router-link to="/" @click="menuOpen=false">首页</router-link>
          <router-link to="/knowledge" @click="menuOpen=false">知识库</router-link>
          <router-link to="/production" @click="menuOpen=false">产区</router-link>
          <router-link to="/wineries" @click="menuOpen=false">酒厂</router-link>
          <router-link to="/news" @click="menuOpen=false">资讯</router-link>
          <router-link to="/profile" @click="menuOpen=false">我的</router-link>
        </nav>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
    <footer class="app-footer">
      <p>&copy; 2026 酱酒研学平台 — 传承千年酱香文化</p>
      <p class="footer-phone-hint" v-if="isMobile">🍶 让更多人懂酱酒</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const menuOpen = ref(false)
const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})
onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', sans-serif;
  background: #FAF8F5;
  -webkit-font-smoothing: antialiased;
}
</style>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  color: #8B4513;
  font-size: 18px;
  cursor: pointer;
  white-space: nowrap;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
  color: #333;
}

.menu-icon {
  font-size: 22px;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-links a {
  color: #555;
  text-decoration: none;
  font-size: 14px;
  padding: 6px 0;
  transition: color 0.2s;
  white-space: nowrap;
}

.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: #8B4513;
  border-bottom: 2px solid #8B4513;
}

.app-main {
  flex: 1;
  padding: 24px 16px;
  background: #FAF8F5;
}

.app-footer {
  background: linear-gradient(180deg, #8B4513 0%, #6B3410 100%);
  color: white;
  padding: 32px 16px;
  text-align: center;
  font-size: 13px;
  line-height: 1.8;
}

.footer-phone-hint {
  margin-top: 8px;
  opacity: 0.7;
}

/* ===== 移动端适配 ===== */
@media (max-width: 767px) {
  .header-inner {
    padding: 10px 12px;
  }

  .logo {
    font-size: 16px;
  }

  .menu-toggle {
    display: block;
  }

  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    flex-direction: column;
    gap: 0;
    padding: 8px 0;
  }

  .nav-links.open {
    display: flex;
  }

  .nav-links a {
    display: block;
    padding: 12px 16px;
    font-size: 15px;
    width: 100%;
    border-bottom: 1px solid #f0f0f0;
  }

  .nav-links a:hover,
  .nav-links a.router-link-exact-active {
    border-bottom: 1px solid #f0f0f0;
    background: #faf5ed;
    color: #8B4513;
  }

  .app-main {
    padding: 16px 12px;
  }
}
</style>
