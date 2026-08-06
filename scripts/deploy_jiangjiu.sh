#!/bin/bash
# 酱酒研学平台部署: dist → docs/ → git 提交推送 (GitHub Pages)
# 用法: bash scripts/deploy_jiangjiu.sh "commit message"
set -e
cd /Users/zhangbing/jiangjiu-platform

MSG="${1:-chore: daily build $(date +%Y-%m-%d)}"

# 1. 清理 docs 旧资源 (保留 .nojekyll)
rm -rf docs/assets docs/images
mkdir -p docs

# 2. 复制新构建
cp -r frontend/dist/* docs/

# 3. 确保 GitHub Pages 需要的 .nojekyll
touch docs/.nojekyll

# 4. 提交推送 (Clash 7897 代理 — 必须 socks5h + HTTP/1.1 + sslVerify=false, 见 SKILL.md pitfalls)
#    纯 http 代理 push 在本机报 LibreSSL SSL_ERROR_SYSCALL / HTTP2 framing error
git add -A
if git diff --cached --quiet; then
  echo "NO_CHANGES — 无变更，跳过提交"
else
  git commit -m "$MSG"
  git -c http.version=HTTP/1.1 -c http.sslVerify=false -c https.proxy=socks5h://127.0.0.1:7897 push origin main
  echo "部署完成: $MSG"
fi
