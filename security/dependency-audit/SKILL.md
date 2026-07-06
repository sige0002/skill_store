---
name: dependency-audit
description: パッケージ・依存関係・サプライチェーンリスクのセキュリティ監査。新しい依存を pip/npm/cargo 等でインストールする前のクイック監査と、依存全体の詳細レビューの2モードを持つ。パッケージインストール時、依存追加のレビュー時、サプライチェーンリスク評価時に使用する。
allowed-tools: Bash, WebSearch, WebFetch, Read
---

# 依存関係セキュリティ監査

新しい依存の追加前に行う**クイック監査**と、プロジェクトの依存全体を対象とする**詳細レビュー**の2モード。パッケージマネージャ経由で新しい依存を追加するときは常にクイック監査をトリガーすること。

## モードA: クイック監査（インストール前）

### 1. タイポスクワッティングのチェック

パッケージ名を有名な人気パッケージと比較する：

- 文字の入れ替え：`requsets` vs `requests`
- ハイフン/アンダースコアの混同：`python-dateutil` vs `python_dateutil`
- プレフィックス/サフィックスの追加：`python-requests` vs `requests`
- 同形異字による置換：`rnumpy`（rn が m に見える）vs `numpy`

比較対象の例 — Python: requests, flask, django, numpy, pandas, scipy, boto3, urllib3, setuptools, cryptography, pillow, pytest, sqlalchemy, pyyaml, jinja2, click, fastapi, pydantic / npm: express, react, lodash, axios, chalk, commander, webpack, typescript, next, vue, uuid, dotenv, jsonwebtoken, mongoose, prisma

人気パッケージと 1〜2 文字しか違わない場合はフラグを立てる。

### 2. レジストリでパッケージを調べる

```bash
# Python（PyPI）
curl -s "https://pypi.org/pypi/<PACKAGE_NAME>/json" | python3 -c "
import sys, json
info = json.load(sys.stdin)['info']
for k in ('name','version','author','license','home_page','summary','requires_python'):
    print(f'{k}: {info.get(k)}')" 2>/dev/null || echo "WARNING: Package not found on PyPI!"

# npm
npm view <PACKAGE_NAME> name version author license homepage description 2>/dev/null || echo "WARNING: Not found on npm!"
```

公式レジストリに見つからない場合は高リスクのシグナル。

### 3. ダウンロード数とメンテナ情報

WebFetch/WebSearch でダウンロード統計（pepy.tech 等）、メンテナ数、パッケージの古さ、最近のリリース活動を確認する。

**リスク指標：**
- 一般的なユーティリティにもかかわらずダウンロード数が非常に少ない（週 100 未満）
- 公開プロフィールのない単独メンテナ
- 作成されて 30 日未満、またはソースリポジトリへのリンクがない
- リリース履歴に大きな空白があり突然活動再開（乗っ取りの可能性）

### 4. 既知の CVE を検索

```bash
# Python
uv run pip-audit 2>/dev/null || echo "pip-audit not available, check manually"
# npm
mkdir -p /tmp/audit-check && cd /tmp/audit-check && \
  echo '{"dependencies":{"<PACKAGE_NAME>":"*"}}' > package.json && npm audit; rm -f package.json
```

さらに WebSearch で `<PACKAGE_NAME> CVE vulnerability` を調べ、GitHub アドバイザリ・https://osv.dev ・https://nvd.nist.gov を確認する。

### 5. ライセンス互換性

- **寛容（一般的に安全）：** MIT、BSD、Apache 2.0、ISC、Unlicense
- **コピーレフト（要レビュー）：** GPL、LGPL、AGPL、MPL — プロジェクトに要件が課される可能性を警告する
- **問題あり：** ライセンス不明、独自の制限的ライセンス

プロジェクトの LICENSE ファイルと照合して互換性を確認する。

## モードB: 詳細レビュー（依存全体・サプライチェーン）

### 1. パッケージソースの検証

- 作者/メンテナの身元と履歴、リポジトリ URL が想定プロジェクトと一致しているか確認する
- プロジェクトのセキュリティポリシ（SECURITY.md）と責任ある開示プロセスの有無を確認する

### 2. サプライチェーンリスク評価

- インストール時のコード実行（任意コードを含む setup.py）・インストール後スクリプトを確認する
- パッケージソースに難読化コードやエンコード文字列がないか確認する
- GitHub のスター数、コントリビュータ、最終コミット日を確認し、12 か月以上更新のないパッケージにフラグを立てる
- 最近新メンテナに移譲されたパッケージにフラグを立てる（乗っ取りリスク）

### 3. 依存ツリー監査

```bash
# Python
uv run pipdeptree -p <package>
uv run pip-licenses --format=table
# Node.js
npm ls --all
```

- 推移的依存とそのリスクプロファイルを特定し、深くネストした/循環依存にフラグを立てる
- 異なるバージョンで重複しているパッケージを確認する

## リスク評価レポート

```
## Security Audit: <PACKAGE_NAME>

| Check | Result | Risk |
|-------|--------|------|
| Typosquatting | [PASS/WARN] | [LOW/MEDIUM/HIGH] |
| Registry presence | [Found/Not Found] | [LOW/HIGH] |
| Download count / maintainer | [details] | [LOW/MEDIUM/HIGH] |
| Known CVEs | [count] | [LOW/MEDIUM/HIGH] |
| License | [license] | [LOW/MEDIUM/HIGH] |
| Supply chain | [details] | [LOW/MEDIUM/HIGH] |

### Overall Risk: [LOW/MEDIUM/HIGH]
### Recommendation: [INSTALL / REVIEW / BLOCK]
```

## 高リスク時の対応

総合評価が **HIGH リスク** の場合：

- **インストールを続行しない**。なぜ高リスクと判断したかを明確に説明する
- 代替案を提案する：より安全な類似パッケージ、または標準ライブラリでの代替
- それでもユーザがインストールを希望する場合は、明示的な確認を求めてリスクを記録する

**自動的に HIGH リスクとするトリガー（1 つ該当で十分）：**
- 公式レジストリに存在しない
- トップ 100 パッケージと 1 文字しか違わない
- 修正が存在しない既知のクリティカル CVE
- ライセンス不明かつソースリポジトリなし
- 公開 7 日未満かつメンテナ履歴なし

## ガイドライン

- デフォルトは慎重側 — 不確実なものは WARN にフラグする
- 怪しいパッケージはインストールせず、レジストリ上でソースをレビューする
- ブラスト半径を考慮する：この依存はプロジェクトにとってどれほど重要か？
