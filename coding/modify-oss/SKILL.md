---
name: modify-oss
description: プロジェクトの規約に従い、テストと PR 準備を含めてオープンソースを改修する。
---

# OSS 改修スキル

以下のリクエストに基づいて OSS を改修する：

**Request:** $ARGUMENTS

## ワークフロー

### Phase 1: コードベース調査
- プロジェクトの README、CONTRIBUTING.md、CODE_OF_CONDUCT.md を読む
- ビルドシステムとパッケージマネージャを特定する（Makefile、setup.py、Cargo.toml など）
- ディレクトリ構造と命名規則を把握する
- 既存のテストフレームワークと実行方法を確認する
- 最近のコミットや PR を見てプロジェクトのスタイルを把握する

### Phase 2: コントリビューションガイドラインの確認
- 必須の CLA（Contributor License Agreement）を確認する
- ブランチ命名規則（feature/、fix/ 等）を確認する
- コミットメッセージの書式（Conventional Commits 等）を確認する
- 必須レビュワーや CI チェックを確認する
- ライセンスが予定する変更と互換であるか確認する

### Phase 3: 環境セットアップ
Python プロジェクトの場合：
```bash
uv venv .venv && source .venv/bin/activate
uv pip install -e ".[dev]"  # or equivalent
```
他の言語はプロジェクトの手順に厳密に従う。

### Phase 4: 実装
- feature ブランチを切る：
  ```bash
  git checkout -b feature/descriptive-name
  ```
- プロジェクトのコードスタイルを厳守する（インデント、命名、インポート）
- 複雑な既存コードの理解には **think hard** を使う
- 変更は最小限・焦点を絞る — 1 関心事に 1 変更
- プロジェクトのスタイルに合わせて docstring・コメントを追加/更新する
- 必要なら設定ファイルを更新する

### Phase 5: テスト
- まず既存テストを実行し、グリーンのベースラインを確認する：
  ```bash
  # Follow the project's test command
  make test  # or pytest, cargo test, npm test, etc.
  ```
- 追加/変更した機能に新しいテストを書く
- 既存テストと新規テストがすべてパスすることを確認する
- プロジェクトの linter/formatter を実行する：
  ```bash
  # Examples — use whatever the project specifies
  uv run ruff check . && uv run ruff format .
  pre-commit run --all-files
  ```

### Phase 6: PR 準備
- 自分の diff を入念にレビューする：
  ```bash
  git diff main...HEAD
  ```
- プロジェクトの規約に従って明確なコミットメッセージを書く
- 各コミットが原子的で自己完結していることを確認する
- PR 説明文を準備する：
  - What：変更の要約
  - Why：動機と文脈
  - How：実装アプローチ
  - Testing：何をどうテストしたか
- 関連 Issue があればリンクする

### Phase 7: 最終チェックリスト
- [ ] 既存テストがすべてパスしている
- [ ] 新機能に新規テストが追加されている
- [ ] プロジェクト規約に従っている
- [ ] 無関係な変更が含まれていない
- [ ] 必要ならドキュメントが更新されている
- [ ] diff にシークレット/認証情報が含まれていない
- [ ] コミット履歴がクリーン

## ガイドライン
- 自分の好みと違っても、プロジェクトの既存パターンを尊重する
- 迷ったらプロジェクト履歴で類似変更がどう行われたかを参照する
- スコープを小さく保つ — 巨大な PR はレビューが難しい
- 明示的なタスクでない限り CI/CD 設定は変更しない
