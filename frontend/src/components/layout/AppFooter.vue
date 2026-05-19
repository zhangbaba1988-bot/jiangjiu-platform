<template>
  <footer class="app-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-logo">
          <h3>酱酒研学平台</h3>
          <p>传承千年酱香文化</p>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2026 酱酒研学平台. All rights reserved.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.app-footer {
  background: linear-gradient(180deg, $primary-color 0%, darken($primary-color, 15%) 100%);
  color: white;
  padding: 40px 0 20px;
  margin-top: 60px;
}

.footer-content {
  text-align: center;
}

.footer-logo {
  margin-bottom: 24px;

  h3 {
    font-size: 20px;
    margin-bottom: 8px;
  }

  p {
    font-size: 14px;
    opacity: 0.8;
  }
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 20px;
  font-size: 13px;
  opacity: 0.7;
}
</style>
