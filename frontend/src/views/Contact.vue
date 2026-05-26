<template>
  <div class="contact-page">
    <section class="hero-card">
      <p class="eyebrow">联系我们</p>
      <h1>{{ content.title }}</h1>
      <p class="subtitle">{{ content.subtitle }}</p>
      <p class="support-note">{{ content.note }}</p>
    </section>

    <section class="contact-grid">
      <article class="info-card">
        <h2>联系方式</h2>
        <div class="contact-item">
          <span>电话</span>
          <a :href="`tel:${content.phone}`">{{ content.phone }}</a>
        </div>
        <div class="contact-item">
          <span>邮箱</span>
          <a :href="`mailto:${content.email}`">{{ content.email }}</a>
        </div>
        <div class="contact-item">
          <span>地址</span>
          <strong>{{ content.address }}</strong>
        </div>
        <div class="contact-item">
          <span>工作时间</span>
          <strong>{{ content.hours }}</strong>
        </div>
      </article>

      <article class="info-card">
        <h2>合作场景</h2>
        <ul class="service-list">
          <li>品牌内容共建与栏目合作</li>
          <li>产区文化活动与线下活动支持</li>
          <li>媒体采访、资料对接与专题报道</li>
          <li>社区运营与用户反馈收集</li>
        </ul>
        <div class="cta-row">
          <a :href="`mailto:${content.email}`" class="primary-btn">发送邮件</a>
          <a href="/jiangjiu-platform/forum" class="secondary-btn">进入论坛</a>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadSiteContent } from '@/utils/siteContent'

const content = ref(loadSiteContent().contact)

onMounted(() => {
  content.value = loadSiteContent().contact
})
</script>

<style scoped>
.contact-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-card,
.info-card {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(139, 69, 19, 0.08);
}

.hero-card {
  padding: 32px;
}

.eyebrow {
  color: #8B4513;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 8px;
}

.hero-card h1 {
  font-size: 30px;
  color: #2f241d;
  margin-bottom: 12px;
}

.subtitle {
  color: #66584d;
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 12px;
}

.support-note {
  color: #8B4513;
  font-weight: 700;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 24px;
}

.info-card {
  padding: 28px;
}

.info-card h2 {
  font-size: 22px;
  color: #2f241d;
  margin-bottom: 16px;
}

.contact-item {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid #f1e7d8;
}

.contact-item span {
  color: #7a6558;
  font-size: 14px;
}

.contact-item a,
.contact-item strong {
  color: #2f241d;
  text-align: right;
  font-size: 14px;
}

.contact-item a {
  text-decoration: none;
  color: #8B4513;
}

.service-list {
  padding-left: 18px;
  color: #4e433b;
  line-height: 2;
}

.cta-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.primary-btn,
.secondary-btn {
  border-radius: 999px;
  padding: 12px 18px;
  text-decoration: none;
  font-weight: 700;
}

.primary-btn {
  color: #fff;
  background: linear-gradient(135deg, #8B4513 0%, #D4AF37 100%);
}

.secondary-btn {
  color: #8B4513;
  background: #f7f1e6;
}

@media (max-width: 767px) {
  .hero-card,
  .info-card {
    padding: 22px;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }

  .contact-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .contact-item a,
  .contact-item strong {
    text-align: left;
  }
}
</style>