<template>
  <div id="app">
    <header style="background:white; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
      <div style="max-width:1200px; margin:0 auto; display:flex; justify-content:space-between; align-items:center;">
        <h1 style="color:#8B4513; margin:0; font-size:20px;">酱酒研学平台</h1>
        <nav style="display:flex; gap:24px;">
          <router-link to="/" style="color:#333; text-decoration:none;">首页</router-link>
          <router-link to="/knowledge" style="color:#333; text-decoration:none;">知识库</router-link>
          <router-link to="/production" style="color:#333; text-decoration:none;">产区</router-link>
          <router-link to="/wineries" style="color:#333; text-decoration:none;">酒厂</router-link>
          <router-link to="/news" style="color:#333; text-decoration:none;">资讯</router-link>
          <router-link to="/profile" style="color:#333; text-decoration:none;">个人中心</router-link>
        </nav>
      </div>
    </header>
    <main style="min-height:70vh; padding:40px 20px; background:#FAF8F5;">
      <div style="max-width:1200px; margin:0 auto;">
        <router-view />
      </div>
    </main>
    <footer style="background:linear-gradient(180deg, #8B4513 0%, #6B3410 100%); color:white; padding:40px 20px; text-align:center;">
      <p>&copy; 2026 酱酒研学平台 - 传承千年酱香文化</p>
    </footer>
  </div>
</template>

<script setup>
console.log('App loaded!')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #FAF8F5;
}
</style>
