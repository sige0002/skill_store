---
name: github-publish
description: リポジトリを GitHub に作成・push・public 化するための手順。「publicでアップして」「ghでリポジトリ作ってpush」「publicに変えて」と言われたときに使用する。公開前の機密スキャン、大容量データの gitignore、コミット著者ポリシーを含む。
---

# GitHub Publish

ローカルリポジトリを GitHub に公開するまでの定型手順。**public 化は取り消しの効かない外部公開**なので、機密スキャンを必ず経由する。

## 手順

### 1. 追跡対象の確認（大容量・生成物を除外）

rosbag・データセット・学習出力・動画などの大容量データは追跡しない：

```bash
# .gitignore に追加してから確認
git check-ignore -v data/ output/ *.mcap *.bag 2>/dev/null
git ls-files | awk -F/ '{print $1}' | sort -u   # 追跡されるトップレベルを目視確認
du -sh $(git ls-files | head -500) 2>/dev/null | sort -rh | head -10  # 大きいファイル検出
```

### 2. 機密スキャン（public 化前に必須）

公開してはいけない情報を全ファイル + git 履歴から検索する：

```bash
# 秘匿語リスト（実機名・社内プロジェクト名・顧客名・IP・トークン等）を決めて全検索
grep -rniE "<secret-word1>|<secret-word2>" --exclude-dir=.git .
# 履歴側も確認（過去のコミットに痕跡が残っていないか）
git log --all -S"<secret-word>" --oneline
git grep "<secret-word>" $(git rev-list --all) 2>/dev/null | head
```

- README・カスタム msg 定義・設定ファイル・コミットメッセージも対象に含める
- **履歴に痕跡がある場合**: 公開前なら履歴を作り直すのが最も確実（`git checkout --orphan` で新規履歴に squash、または filter-repo）。公開後の削除は不完全になりがち
- 機体固有・社外秘の設定は `config/local/` 等に分離して gitignore する（layered-config スキル参照）

### 3. コミット著者ポリシー

- コミットメッセージに `Co-Authored-By: Claude ...` トレーラを**入れない**
- AI の関与を示したい場合はリポジトリの CONTRIBUTORS や README に記載する方式にする

### 4. 公開前の品質ゲート

```bash
uvx ruff check . && uvx ruff format --check .   # Python
uv run pytest -x -q                              # テストがあれば
```

### 5. リポジトリ作成 & push

```bash
gh auth status                                   # 認証確認
gh repo create <name> --public --source=. --push # 新規作成 + push
# 既存リポジトリの場合
git push -u origin main
```

### 6. 可視性の変更（private → public）

```bash
gh repo edit <owner>/<name> --visibility public --accept-visibility-change-consequences
gh repo view <owner>/<name> --json visibility,url   # 確認
```

## チェックリスト

- [ ] 大容量データ・生成物が .gitignore されている
- [ ] 秘匿語スキャンをワーキングツリーと**履歴の両方**に実施した
- [ ] コミットに Claude の Co-Author トレーラが入っていない
- [ ] lint / テストがパスしている
- [ ] README がリポジトリの内容を正しく説明している（内部事情の漏れがない）
- [ ] public 化後に URL を報告する
