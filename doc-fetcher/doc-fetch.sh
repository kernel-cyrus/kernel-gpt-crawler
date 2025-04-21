#!/bin/bash

# 设置变量
REPO_URL="https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"
DIR_PATH="Documentation"     # 改成你想要下载的目录，比如 kernel, fs, etc.
BRANCH="master"   # torvalds 的分支名是 master
CLONE_DIR="docs"

# 克隆仓库（使用稀疏模式）
git clone --filter=blob:none --no-checkout --depth=1 "$REPO_URL" "$CLONE_DIR"
cd "$CLONE_DIR"

# 启用 sparse-checkout
git sparse-checkout init --cone
git sparse-checkout set "$DIR_PATH"
git checkout "$BRANCH"

echo "✅ 目录 $DIR_PATH 已下载到 $(pwd)/$DIR_PATH"
