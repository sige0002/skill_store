---
name: branch-cleanup
description: 作業ブランチの統合とマージ済みブランチの削除、fork の upstream 整理を行う手順。「ブランチを整理して」「developに統合して使ってないのは消して」「マージ済みブランチを削除」と言われたときに使用する。
---

# Branch Cleanup

作業ブランチが増えてきたときの統合・整理の定型手順。**マージされていない作業を消さない**ことが最重要。

## 手順

### 1. 現状把握

```bash
git branch -a --sort=-committerdate          # ローカル+リモート、新しい順
git branch --merged main                     # main にマージ済み（削除候補）
git branch --no-merged main                  # 未マージ（要確認）
git worktree list                            # worktree が掴んでいるブランチは削除不可
```

### 2. 統合ブランチへの集約（必要な場合）

```bash
git checkout -b develop main    # 統合先を用意（既にあれば checkout のみ）
git merge --no-ff feature/xxx   # 各作業ブランチを順に統合
# コンフリクトは1ブランチずつ解消し、都度テストを回す
```

### 3. マージ済みブランチの削除

```bash
# ローカル
git branch -d feature/xxx        # -d はマージ済みのみ削除できる安全側。-D は使う前に必ず未マージ内容を確認
# リモート
git push origin --delete feature/xxx
# リモート追跡の掃除
git fetch --prune
```

### 4. fork 運用時の upstream 整理

追跡ブランチを main だけに絞ると fetch が軽くなり、混乱も減る：

```bash
git remote set-branches upstream main
git fetch upstream --prune
```

## 原則

- `--no-merged` に出たブランチは**中身を確認してから**判断する（`git log main..branch --oneline`）
- リモート削除は共同作業者に影響する — 自分以外が使っている可能性があれば先に確認する
- worktree が checkout 中のブランチは先に `git worktree remove` する
- 削除前に最終防衛線として `git branch backup/<name> <name>` を切る選択肢もある（大掃除のとき）
