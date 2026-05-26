const STORAGE_KEY = 'jiangjiu_site_content'

export const defaultSiteContent = () => ({
  hero: {
    title: '探索酱酒文化的奥秘',
    description: '传承千年酿造工艺，品味酱香独特魅力',
    ctaText: '了解更多',
    ctaLink: '/knowledge'
  },
  contact: {
    title: '联系我们',
    subtitle: '欢迎企业合作、内容对接、媒体采访与市场交流。',
    phone: '400-820-9918',
    email: 'contact@jiangjiu-platform.com',
    address: '贵州省贵阳市南明区酱香文化园区',
    hours: '周一至周五 9:00-18:00',
    note: '我们将尽快回复你的咨询，并为你提供更精准的内容与合作建议。'
  },
  forum: {
    title: '酱酒论坛',
    subtitle: '在这里分享品鉴心得、交流产区资讯、讨论行业热点。',
    intro: '论坛为酱酒爱好者、行业从业者和品牌合作方提供交流空间，欢迎持续参与。',
    topics: [
      {
        title: '如何判断一款酱酒是否适合长期收藏？',
        author: '老酒收藏者',
        category: '品鉴交流',
        replies: 18,
        lastActive: '2小时前'
      },
      {
        title: '品牌方如何做好产区文化内容运营？',
        author: '内容运营专员',
        category: '内容合作',
        replies: 11,
        lastActive: '今天 10:30'
      },
      {
        title: '新国标对传统工艺与市场营销有哪些影响？',
        author: '行业观察员',
        category: '政策解读',
        replies: 9,
        lastActive: '昨天'
      }
    ]
  },
  permissions: [
    '首页文案与入口维护',
    '联系我们信息更新',
    '论坛内容与置顶话题维护'
  ]
})

const sanitizeContent = (content) => {
  const fallback = defaultSiteContent()

  return {
    hero: {
      ...fallback.hero,
      ...content?.hero
    },
    contact: {
      ...fallback.contact,
      ...content?.contact
    },
    forum: {
      ...fallback.forum,
      ...content?.forum,
      topics: Array.isArray(content?.forum?.topics) && content.forum.topics.length
        ? content.forum.topics
        : fallback.forum.topics
    },
    permissions: Array.isArray(content?.permissions) && content.permissions.length
      ? content.permissions
      : fallback.permissions
  }
}

export const loadSiteContent = () => {
  if (typeof localStorage === 'undefined') {
    return defaultSiteContent()
  }

  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return defaultSiteContent()
    }

    const parsed = JSON.parse(raw)
    return sanitizeContent(parsed)
  } catch (error) {
    console.warn('解析站点内容失败，已回退默认值', error)
    return defaultSiteContent()
  }
}

export const saveSiteContent = (content) => {
  if (typeof localStorage === 'undefined') {
    return
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(sanitizeContent(content)))
}

export const getSiteContent = () => loadSiteContent()
