#!/usr/bin/env python3
"""在 github.com:443 被代理拦截、但 api.github.com 可达时，用 GitHub REST API 推送本地最新提交。

用法:
    git add -A && git commit -m "..."
    python3 scripts/push_via_github_api.py "提交说明"

原理: 取 HEAD~1..HEAD 的 diff → 逐个文件建 blob → 基于远端当前 tree 建新 tree
      → 建 commit → PATCH refs/heads/main。重命名按「新路径加 blob + 旧路径 sha=null」。
前提: gh 已登录（gh auth token 可取到），api.github.com 可经代理访问。
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

REPO = "zhangbaba1988-bot/jiangjiu-platform"
ROOT = "/Users/zhangbing/jiangjiu-platform"
PROXY = os.environ.get("HTTPS_PROXY", "http://127.0.0.1:7897")
MSG = sys.argv[1] if len(sys.argv) > 1 else subprocess.run(
    ["git", "log", "-1", "--pretty=%s"], cwd=ROOT, capture_output=True, text=True).stdout.strip()

TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"https": PROXY, "http": PROXY}))


def api(path, method="GET", payload=None):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method,
        headers={
            "Authorization": "Bearer " + TOKEN,
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "hermes-agent",
        },
    )
    with opener.open(req, timeout=60) as r:
        body = r.read().decode()
    return json.loads(body) if body else {}


def main():
    ref = api(f"/repos/{REPO}/git/ref/heads/main")
    parent_sha = ref["object"]["sha"]
    base_tree = api(f"/repos/{REPO}/git/commits/{parent_sha}")["tree"]["sha"]
    print("远端 parent:", parent_sha[:7])

    diff = subprocess.run(["git", "diff", "--name-status", "-M", "HEAD~1", "HEAD"],
                          cwd=ROOT, capture_output=True, text=True).stdout.strip().split("\n")
    entries = []
    for line in diff:
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("D"):
            entries.append({"path": parts[1], "mode": "100644", "type": "blob", "sha": None})
            continue
        if status.startswith("R"):
            entries.append({"path": parts[1], "mode": "100644", "type": "blob", "sha": None})
            path = parts[2]
        else:
            path = parts[1]
        blob = api(f"/repos/{REPO}/git/blobs", "POST", {
            "content": base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode(),
            "encoding": "base64",
        })
        entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

    tree = api(f"/repos/{REPO}/git/trees", "POST", {"base_tree": base_tree, "tree": entries})
    commit = api(f"/repos/{REPO}/git/commits", "POST",
                 {"message": MSG, "tree": tree["sha"], "parents": [parent_sha]})
    api(f"/repos/{REPO}/git/refs/heads/main", "PATCH", {"sha": commit["sha"], "force": False})
    print("已推送 commit:", commit["sha"], "| 文件变更:", len(entries))


if __name__ == "__main__":
    main()
