#!/usr/bin/env python3
"""同步 knowledge.json → 前端 fallback (Knowledge.vue 列表 + KnowledgeDetail.vue 详情)。

GitHub Pages 是纯静态站点、无后端 API，前端在 API 不可达时回退到硬编码数组。
只改 backend/data/knowledge.json 不会反映到线上站点 —— 必须跑本脚本并重新 build。

用法: python3 scripts/sync_kb_to_frontend.py   (在 jiangjiu-platform-final 仓库根目录)
验证: grep -c "id:'klg_" frontend/src/views/Knowledge.vue   # 应等于文章总数
"""
import json
import re
import sys
import os

REPO = '/Users/zhangbing/jiangjiu-platform'
KB_PATH = os.path.join(REPO, 'backend/data/knowledge.json')
KNOWLEDGE_VUE = os.path.join(REPO, 'frontend/src/views/Knowledge.vue')
DETAIL_VUE = os.path.join(REPO, 'frontend/src/views/KnowledgeDetail.vue')


def esc(s):
    """转义单引号/反引号/换行，安全嵌入 JS 字符串/模板串。"""
    return (s or '').replace("\\", "\\\\").replace("'", "\\'").replace('`', '\\`').replace('\n', ' ')


def main():
    with open(KB_PATH, encoding='utf-8') as f:
        kb = json.load(f)
    print(f'knowledge.json 文章数: {len(kb)}')

    # 1. Knowledge.vue fallback 列表 (单引号字符串)
    lines = []
    for a in kb:
        icon = a.get('icon', '📄')
        lines.append(
            f"      {{id:'{esc(a['id'])}',title:'{esc(a['title'])}',category:'{esc(a['category'])}',"
            f"icon:'{icon}',summary:'{esc(a.get('summary',''))}',views:{a.get('views', 0)}}},"
        )
    fallback_block = '\n'.join(lines)

    with open(KNOWLEDGE_VUE, encoding='utf-8') as f:
        ksrc = f.read()
    pattern = re.compile(r'(catch \(e\) \{\n\s*allArticles\.value = \[).*?(\]\n\s*\} finally)', re.DOTALL)
    if not pattern.search(ksrc):
        print('ERROR: 未找到 Knowledge.vue fallback 数组模式'); sys.exit(1)
    new_ksrc = pattern.sub(lambda m: m.group(1) + '\n' + fallback_block + '\n' + m.group(2), ksrc)
    with open(KNOWLEDGE_VUE, 'w', encoding='utf-8') as f:
        f.write(new_ksrc)
    print(f'Knowledge.vue fallback 已更新: {len(kb)} 篇')

    # 2. KnowledgeDetail.vue localArticles (反引号模板串，content 含 markdown)
    detail_entries = []
    for a in kb:
        detail_entries.append(
            f"      '{esc(a['id'])}': {{ id: '{esc(a['id'])}', title: `{esc(a['title'])}`, "
            f"author: `{esc(a.get('author','酱酒知识库'))}`, icon: `{a.get('icon','📄')}`, "
            f"views: {a.get('views', 0)}, content: `{esc(a.get('content',''))}` }},"
        )
    detail_block = '\n'.join(detail_entries)

    with open(DETAIL_VUE, encoding='utf-8') as f:
        dsrc = f.read()
    dpattern = re.compile(r"(const localArticles = \{\n).*?(\n    \}\n    const local = localArticles)", re.DOTALL)
    if not dpattern.search(dsrc):
        print('ERROR: 未找到 KnowledgeDetail.vue localArticles 模式'); sys.exit(1)
    new_dsrc = dpattern.sub(lambda m: m.group(1) + detail_block + m.group(2), dsrc)
    with open(DETAIL_VUE, 'w', encoding='utf-8') as f:
        f.write(new_dsrc)
    print(f'KnowledgeDetail.vue localArticles 已更新: {len(kb)} 篇')


if __name__ == '__main__':
    main()
