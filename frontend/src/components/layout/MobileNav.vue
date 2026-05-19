<template>
  <nav class="mobile-nav">
    <router-link 
      v-for="item in navItems" 
      :key="item.path"
      :to="item.path"
      class="nav-item"
      :class="{ active: $route.path === item.path }"
    >
      <span class="nav-label">{{ item.name }}</span>
    </router-link>
  </nav>
</template>

<script setup>
const navItems = [
  { path: '/', name: '首页' },
  { path: '/knowledge', name: '知识库' },
  { path: '/production', name: '产区' },
  { path: '/wineries', name: '酒厂' },
  { path: '/profile', name: '我的' }
]
</script>

<style lang="scss" scoped>
.mobile-nav {
  display: flex;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  padding: 8px 0;
  z-index: 99;

  @include respond-to(desktop) {
    display: none;
  }

  .nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    color: $text-light;
    text-decoration: none;
    font-size: 12px;

    &.active {
      color: $primary-color;
    }
  }

  .nav-label {
    margin-top: 4px;
  }
}
</style>
