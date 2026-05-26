<template>
  <div class="article-detail">
    <button class="back-btn" @click="$router.back()">← 返回列表</button>
    
    <div v-if="loading" class="state-box">
      <div class="state-icon">⏳</div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="state-box">
      <div class="state-icon">⚠️</div>
      <p class="error-text">{{ error }}</p>
    </div>

    <article v-else class="article-card">
      <header class="article-header">
        <span class="article-icon">{{ article.icon || '📖' }}</span>
        <h1>{{ article.title }}</h1>
        <div class="article-meta">
          <span>{{ formatViews(article.views) }} 阅读</span>
        </div>
      </header>
      
      <div class="article-body" v-html="renderedContent"></div>

      <footer class="article-footer"></footer>
    </article>

    <!-- ========== 获客转化模块 ========== -->
    <div class="cta-section">
      <div class="cta-divider"><span>🍶 想要品鉴正宗酱酒？</span></div>
      
      <div class="cta-products">
        <div class="cta-product">
          <span class="cta-p-icon">🛢️</span>
          <div class="cta-p-info"><strong>君范·雅藏 y5</strong><span>5年坤沙 · 入门首选</span></div>
          <span class="cta-p-price">¥198/桶</span>
        </div>
        <div class="cta-product">
          <span class="cta-p-icon">🏺</span>
          <div class="cta-p-info"><strong>君范·典藏 y10</strong><span>10年坤沙 · 酒友钟爱</span></div>
          <span class="cta-p-price">¥398/桶</span>
        </div>
        <div class="cta-product">
          <span class="cta-p-icon">👑</span>
          <div class="cta-p-info"><strong>君范·臻藏 y14</strong><span>14年坤沙 · 品鉴级</span></div>
          <span class="cta-p-price">¥698/桶</span>
        </div>
      </div>

      <div class="cta-contact">
        <div class="cta-qr">
          <img src="/qr-wechat.png" alt="微信二维码" class="cta-qr-img" />
          <div>
            <strong>👤 兵哥微信号：bingge_jiangjiu</strong>
            <p>加微信备注"知识库"，秒通过</p>
          </div>
        </div>
        <div class="cta-actions">
          <button class="cta-btn" @click="copyWechat">📋 复制微信号</button>
          <button class="cta-btn cta-btn-primary" @click="contactVisible = true">💬 立即咨询</button>
        </div>
        <div v-if="contactVisible" class="cta-contact-info">
          <p>📱 微信搜索：<strong>bingge_jiangjiu</strong></p>
          <p>📝 备注：<strong>知识库</strong></p>
          <p style="margin-top:6px;font-size:12px;opacity:.7">或扫描左侧二维码直接添加</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { knowledgeApi } from '@/api'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const article = ref({ title: '加载中...', views: 0, content: '' })
const contactVisible = ref(false)

const copyWechat = () => {
  navigator.clipboard.writeText('bingge_jiangjiu').then(() => {
    alert('微信号已复制！打开微信搜索添加')
  }).catch(() => {
    alert('微信号：bingge_jiangjiu')
  })
}

const formatViews = (v) => v >= 10000 ? (v/10000).toFixed(1)+'万' : String(v||0)

const parseMarkdown = (text) => {
  if (!text || typeof text !== 'string') return ''
  
  let html = text
    // Headers: ## → h3, ### → h4
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // List items
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // Tables (simple: convert rows with |)
    .replace(/^\|(.+)\|$/gm, (match) => {
      const cells = match.split('|').filter(c => c.trim())
      if (cells.length >= 2) {
        return '<div class="data-row"><span>' + cells.map(c => c.trim()).join('</span><span>') + '</span></div>'
      }
      return match
    })
    // Separators (---|---)
    .replace(/^\|[-| ]+\|$/gm, '')
    // Blockquotes
    .replace(/^\* (.+)$/gm, '<blockquote>$1</blockquote>')
    // Paragraphs (double newline)
    .replace(/\n\n/g, '</p><p>')
    // Single newlines
    .replace(/\n/g, '<br>')
  
  // Wrap lists
  html = html.replace(/(<li>.*?<\/li>)/gs, (match) => {
    if (!match.includes('</ul>')) {
      return '<ul>' + match + '</ul>'
    }
    return match
  })
  
  // Clean up empty <p>s
  html = html.replace(/<p><\/p>/g, '')
  html = html.replace(/<p><br><\/p>/g, '')
  
  return '<p>' + html + '</p>'
}

const renderedContent = computed(() => {
  return parseMarkdown(article.value.content)
})

onMounted(async () => {
  try {
    const res = await knowledgeApi.getDetail(route.params.id)
    if (res.code === 200 && res.data) {
      article.value = res.data
    } else {
      article.value = { title: '文章不存在', author: '', views: 0, content: '抱歉，您访问的文章不存在。' }
    }
  } catch (e) {
    // 后端不可用时使用本地数据
    const localArticles = {
      'klg_043': { id: 'klg_043', title: `抖音金黄桶装酱酒是真老酒吗？新国标说清楚了`, author: `酱香荟`, icon: `🛢️`, views: 5800, content: `最近很多酒友私信：抖音上透明塑料桶装的酱香酒，颜色金黄透亮，看着像陈年老酒，这种黄是自然的，还是加了东西？

今天结合最新国标GB/T 10781.4-2024，把桶装酱酒颜色猫腻、塑料存酒风险一次性讲透。

## 一、新国标：正宗酱香酒该是什么颜色？

新国标GB/T 10781.4-2024（2025-06-01实施）明确：
- 酱香型白酒：清澈、透明、无色或微黄，无沉淀、无悬浮物
- 严禁添加焦糖色、合成色素、香精、甜味剂
- 不得添加食用酒精及非发酵呈香呈味物质

微黄来自长期储存中天然联酮类物质，随年份缓慢加深：3-5年极淡微黄；10年+略深但依然清亮通透。

**真老酒是清浅微黄，不是深金黄、浓茶黄。**抖音桶装酒那种金黄浓郁，大概率是新酒+人工色素。

## 二、塑料桶装酒：安全隐患

普通塑料桶耐热差，暴晒/高温→塑化剂析出溶进酒里。酱酒活性物质多，长期接触塑料会腐蚀桶壁、带入塑胶臭，破坏酱香层次。存酒应用陶坛、玻璃、食品级不锈钢。

## 三、新国标重点：买酱酒认准这3点

1. **标准号**：2025-06-01后认准GB/T 10781.4-2024
2. **工艺标注**：优选酱香型白酒（大曲），12987工艺
3. **色泽判断**：清澈微黄、通透干净；颜色过黄有塑胶味→直接pass

## 四、总结

颜色≠年份。金黄多是调色，清浅微黄才是真年份本色。坚决不用塑料桶存酒。新国标落地后，无添加、纯固态、工艺透明才是趋势。` },
    }
    const local = localArticles[route.params.id]
    if (local) {
      article.value = local
    } else {
      article.value = { title: '文章不存在', author: '', views: 0, content: '抱歉，您访问的文章不存在。' }
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.article-detail {
  max-width: 760px;
  margin: 0 auto;
  padding: 20px 16px 60px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: 1px solid #ddd;
  padding: 8px 20px;
  border-radius: 20px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 24px;
  transition: all 0.2s;
}
.back-btn:hover {
  border-color: #8B4513;
  color: #8B4513;
}

.state-box {
  text-align: center;
  padding: 100px 0;
  color: #999;
}
.state-icon {
  font-size: 48px;
  margin-bottom: 12px;
}
.error-text {
  color: #e74c3c;
}

.article-card {
  background: #fff;
  border-radius: 12px;
  padding: 48px 48px 40px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.article-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid #f0f0f0;
}
.article-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}
.article-header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.5;
  margin: 0 0 16px;
}
.article-meta {
  font-size: 14px;
  color: #999;
}
.article-meta .dot {
  margin: 0 8px;
}

.article-body {
  font-size: 15px;
  line-height: 1.8;
  color: #444;
}

.article-body :deep(h3) {
  font-size: 18px;
  font-weight: 600;
  color: #8B4513;
  margin: 36px 0 12px;
  padding-left: 12px;
  border-left: 3px solid #D4AF37;
}
.article-body :deep(h4) {
  font-size: 16px;
  font-weight: 600;
  color: #555;
  margin: 24px 0 8px;
}
.article-body :deep(p) {
  margin: 0 0 12px;
}
.article-body :deep(strong) {
  color: #333;
  font-weight: 600;
}
.article-body :deep(em) {
  color: #8B4513;
  font-style: normal;
}

.article-body :deep(ul) {
  padding: 0 0 0 20px;
  margin: 8px 0 16px;
}
.article-body :deep(li) {
  margin-bottom: 6px;
  padding-left: 4px;
  list-style: none;
  position: relative;
}
.article-body :deep(li)::before {
  content: '·';
  position: absolute;
  left: -16px;
  color: #D4AF37;
  font-weight: bold;
}

.article-body :deep(.data-row) {
  display: flex;
  padding: 8px 12px;
  border-bottom: 1px solid #f5f5f5;
  font-size: 14px;
}
.article-body :deep(.data-row span) {
  flex: 1;
}
.article-body :deep(.data-row:first-child) {
  font-weight: 600;
  color: #8B4513;
  background: #faf8f5;
  border-radius: 6px 6px 0 0;
}

.article-body :deep(blockquote) {
  margin: 20px 0;
  padding: 14px 20px;
  background: #faf8f5;
  border-left: 3px solid #D4AF37;
  color: #8B4513;
  font-size: 14px;
  border-radius: 0 6px 6px 0;
}

.article-footer {
  margin-top: 12px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  font-size: 12px;
  color: #bbb;
  text-align: center;
}

/* 获客转化模块 */
.cta-section {
  margin-top: 40px;
  border-top: 2px dashed #D4AF37;
  padding-top: 24px;
}
.cta-divider {
  text-align: center;
  margin-bottom: 20px;
  position: relative;
}
.cta-divider span {
  background: #fff;
  padding: 0 16px;
  font-size: 16px;
  font-weight: 600;
  color: #8B4513;
}
.cta-products {
  background: linear-gradient(135deg, #faf8f5, #fef9e7);
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 16px;
}
.cta-product {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
}
.cta-product:last-child { border-bottom: none; }
.cta-p-icon { font-size: 28px; }
.cta-p-info { flex: 1; }
.cta-p-info strong { display: block; font-size: 14px; color: #333; margin-bottom: 2px; }
.cta-p-info span { font-size: 12px; color: #999; }
.cta-p-price { font-size: 15px; font-weight: 700; color: #e17055; white-space: nowrap; }

.cta-contact {
  background: linear-gradient(135deg, #8B4513, #A0522D);
  border-radius: 10px;
  padding: 18px;
  color: #fff;
}
.cta-qr {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}
.cta-qr-img {
  width: 72px;
  height: 72px;
  border-radius: 6px;
  border: 2px solid rgba(255,255,255,.3);
  flex-shrink: 0;
}
.cta-qr-icon { font-size: 40px; }
.cta-qr strong { font-size: 15px; display: block; margin-bottom: 2px; }
.cta-qr p { font-size: 12px; opacity: .85; margin: 0; }

.cta-actions {
  display: flex;
  gap: 10px;
}
.cta-btn {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,.3);
  background: rgba(255,255,255,.15);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: .2s;
}
.cta-btn:hover { background: rgba(255,255,255,.25); }
.cta-btn-primary {
  background: #D4AF37;
  border-color: #D4AF37;
  color: #333;
}
.cta-btn-primary:hover { background: #e6c14a; }

.cta-contact-info {
  margin-top: 14px;
  padding: 12px;
  background: rgba(255,255,255,.15);
  border-radius: 8px;
  text-align: center;
}
.cta-contact-info p { margin: 0; font-size: 14px; }
.cta-contact-info strong { color: #D4AF37; }
</style>
