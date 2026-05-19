import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/Knowledge.vue'),
    meta: { title: '知识库' }
  },
  {
    path: '/knowledge/:id',
    name: 'KnowledgeDetail',
    component: () => import('@/views/KnowledgeDetail.vue'),
    meta: { title: '文章详情' }
  },
  {
    path: '/production',
    name: 'Production',
    component: () => import('@/views/Production.vue'),
    meta: { title: '产区数据' }
  },
  {
    path: '/production/:id',
    name: 'ProductionDetail',
    component: () => import('@/views/ProductionDetail.vue'),
    meta: { title: '产区详情' }
  },
  {
    path: '/wineries',
    name: 'Wineries',
    component: () => import('@/views/Wineries.vue'),
    meta: { title: '酒厂名录' }
  },
  {
    path: '/wineries/:id',
    name: 'WineryDetail',
    component: () => import('@/views/WineryDetail.vue'),
    meta: { title: '酒厂详情' }
  },
  {
    path: '/news',
    name: 'News',
    component: () => import('@/views/News.vue'),
    meta: { title: '行业资讯' }
  },
  {
    path: '/news/:id',
    name: 'NewsDetail',
    component: () => import('@/views/NewsDetail.vue'),
    meta: { title: '资讯详情' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '个人中心' }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/Search.vue'),
    meta: { title: '搜索' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '酱酒研学平台'} - 传承千年酱香文化`
  next()
})

export default router
