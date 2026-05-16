/**
 * 页面统计分析服务
 * 追踪用户页面访问，发送数据到后端
 * 支持去重和频率限制，避免虚假浏览量
 */

const STORAGE_KEY = 'analytics_session';
const VIEW_CACHE_KEY = 'analytics_view_cache';  // 去重缓存
const VIEW_EXPIRE_MS = 5 * 60 * 1000;  // 同一页面5分钟内不重复记录

// 生成或获取会话ID
function getSessionId() {
  let sessionId = localStorage.getItem(STORAGE_KEY);
  if (!sessionId) {
    sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substring(2, 15);
    localStorage.setItem(STORAGE_KEY, sessionId);
  }
  return sessionId;
}

// 获取视图缓存
function getViewCache() {
  try {
    const cache = localStorage.getItem(VIEW_CACHE_KEY);
    return cache ? JSON.parse(cache) : {};
  } catch {
    return {};
  }
}

// 保存视图缓存
function saveViewCache(cache) {
  try {
    // 清理过期数据
    const now = Date.now();
    const cleaned = {};
    for (const [key, timestamp] of Object.entries(cache)) {
      if (now - timestamp < VIEW_EXPIRE_MS * 2) {
        cleaned[key] = timestamp;
      }
    }
    localStorage.setItem(VIEW_CACHE_KEY, JSON.stringify(cleaned));
  } catch (e) {
    console.warn('Failed to save view cache:', e);
  }
}

// 检查是否应该记录此浏览（去重）
function shouldRecordView(path, contentType, contentId) {
  const now = Date.now();
  const cache = getViewCache();
  
  // 生成唯一键：会话ID + 页面路径
  const sessionId = getSessionId();
  const cacheKey = `${sessionId}:${path}`;
  
  // 检查上次记录时间
  if (cache[cacheKey] && (now - cache[cacheKey]) < VIEW_EXPIRE_MS) {
    return false;  // 5分钟内已记录，跳过
  }
  
  // 更新缓存
  cache[cacheKey] = now;
  saveViewCache(cache);
  return true;
}

// 追踪队列，用于批量发送
let trackQueue = [];
let isProcessing = false;
let flushTimer = null;

/**
 * 追踪页面访问
 * @param {string} contentType - 内容类型: 'home', 'game', 'article'
 * @param {number|null} contentId - 内容ID（如果是游戏或文章页面）
 */
export function trackPageView(contentType = null, contentId = null) {
  const path = window.location.pathname;
  
  // 跳过管理员页面浏览记录
  if (path.startsWith('/admin')) {
    return;  // 管理员页面不记录浏览量
  }
  
  // 去重检查
  if (!shouldRecordView(path, contentType, contentId)) {
    return;  // 跳过重复记录
  }
  
  const data = {
    content_type: contentType,
    content_id: contentId,
    path: path,
    timestamp: Date.now(),
    referrer: document.referrer || null,
    session_id: getSessionId(),
    user_agent: navigator.userAgent.substring(0, 200)  // 截取前200字符
  };

  // 添加到队列
  trackQueue.push(data);

  // 限制队列大小，防止内存溢出
  if (trackQueue.length > 50) {
    trackQueue = trackQueue.slice(-50);
  }

  // 延迟发送，避免频繁请求
  if (flushTimer) {
    clearTimeout(flushTimer);
  }
  flushTimer = setTimeout(() => {
    flushQueue();
  }, 3000);  // 3秒后发送
}

/**
 * 批量发送追踪数据
 */
async function flushQueue() {
  if (isProcessing || trackQueue.length === 0) return;
  
  isProcessing = true;
  const dataToSend = [...trackQueue];
  trackQueue = [];

  try {
    const response = await fetch('/api/analytics/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ views: dataToSend }),
      keepalive: true
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
  } catch (error) {
    console.warn('Analytics flush failed:', error.message);
    // 发送失败时不放回队列，避免重复记录
    // 如果真的很重要，可以使用sendBeacon作为后备
    try {
      const blob = new Blob([JSON.stringify({ views: dataToSend })], { type: 'application/json' });
      navigator.sendBeacon('/api/analytics/batch', blob);
    } catch (e) {
      console.warn('sendBeacon also failed');
    }
  }

  isProcessing = false;
}

/**
 * 页面卸载时发送剩余数据
 */
export function initAnalytics() {
  // 页面卸载前发送剩余数据
  window.addEventListener('beforeunload', () => {
    if (trackQueue.length > 0) {
      const blob = new Blob([JSON.stringify({ views: trackQueue })], { type: 'application/json' });
      navigator.sendBeacon('/api/analytics/batch', blob);
    }
  });

  // 页面隐藏时也发送（如切换标签页）
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden' && trackQueue.length > 0) {
      const blob = new Blob([JSON.stringify({ views: trackQueue })], { type: 'application/json' });
      navigator.sendBeacon('/api/analytics/batch', blob);
      trackQueue = [];
    }
  });

  // Vue Router 导航时追踪
  if (window.router) {
    window.router.afterEach((to) => {
      // 跳过管理员页面
      if (to.path.startsWith('/admin')) {
        return;
      }
      
      // 根据路由判断内容类型
      let contentType = 'home';
      let contentId = null;

      if (to.path.startsWith('/games/')) {
        contentType = 'game';
        contentId = to.params.id ? parseInt(to.params.id) : null;
      } else if (to.path.startsWith('/articles/')) {
        contentType = 'article';
        contentId = to.params.id ? parseInt(to.params.id) : null;
      } else if (to.path === '/games') {
        contentType = 'games';
      } else if (to.path === '/articles') {
        contentType = 'articles';
      }

      trackPageView(contentType, contentId);
    });
  }
}

// 主动刷新一次（页面加载时）
export function recordPageLoad() {
  trackPageView('home', null);
}

// 手动记录游戏/文章浏览
export function recordContentView(contentType, contentId) {
  trackPageView(contentType, contentId);
}

export default {
  trackPageView,
  initAnalytics,
  recordPageLoad,
  recordContentView,
  getSessionId
};
