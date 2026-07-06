---
name: layered-config
description: ポート・ホスト・機体名などのハードコードを排除し、.env とカテゴリ別 config ディレクトリに外部化する手順。「ポートがハードコードされている」「設定を.envに逃がして」「機体ごとの設定を分けたい」「機密設定をgitに乗せたくない」ときに使用する。
---

# Layered Config（設定の外部化と機密ローカル分離）

ハードコードされた環境依存値（ポート・ホスト・デバイス名・機体名）を発見・外部化し、環境/用途/機体の3層で管理するパターン。環境依存値がコードに埋まっていると、機体の追加・ポート変更のたびに全ファイル修正が必要になり、機密（実機名など）が公開リポジトリに漏れる原因にもなる。

## 1. ハードコードの精査

```bash
# ポート・IP・ホスト名の埋め込みを全検索（Makefile・compose・フロントも対象）
grep -rniE "localhost:[0-9]{4}|:(8[0-9]{3}|3[0-9]{3})|192\.168\.|10\.0\." \
  --exclude-dir={.git,node_modules,.venv} .
# 機体名・デバイス名の埋め込み
grep -rniE "<robot-name>|/dev/tty|video[0-9]" --exclude-dir={.git,node_modules,.venv} .
```

Makefile の表示メッセージや docs 内の URL も忘れずに対象にする（実行時だけでなく「表示」のハード依存も混乱のもと）。

## 2. 3層構成

```
.env                  # 環境層: ポート、ホスト、ROS_DOMAIN_ID、既定で使う config の指定
.env.example          # コミットする見本（実値の代わりに例とコメント）
config/
├── robot/            # 用途層: カテゴリ別に yaml を分ける
├── record/
├── validation/
├── stream/
└── local/            # 機体層: 機体固有・社外秘 → .gitignore 対象
```

- **`.env` が「どの config を使うか」を決める**（例: `ROBOT_CONFIG=config/robot/sim.yaml`）。コードは env 経由でのみ設定を読む
- **`config/local/` は gitignore** し、実機名・キャリブレーション値・接続先など公開できない値はここに置く
- UI から設定を選ばせる場合は、カテゴリディレクトリの一覧をそのままプルダウン候補にする（一覧＝ディレクトリ走査にすると追加が自動反映）

## 3. `.env.example` の書き方

実値ではなく「例 + 選択肢のコメント」を書く。初見の人がコピーしてすぐ動かせる状態にする：

```bash
# バックエンド API ポート
API_PORT=8000
# ROS 2 の DDS ドメイン（全コンテナ・ホストで一致させること）
ROS_DOMAIN_ID=0
# DDS 実装: rmw_cyclonedds_cpp（既定） / rmw_fastrtps_cpp
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# 使用するロボット設定（config/robot/ から選ぶ。実機用は config/local/ に置く）
ROBOT_CONFIG=config/robot/sim.yaml
```

## 4. 移行手順

1. grep で全ハードコード箇所をリスト化する（上記コマンド）
2. `.env` + 読み込み口（compose の `env_file`、アプリの settings モジュール、Makefile の `include .env`）を先に用意する
3. 1箇所ずつ env 参照に置換し、都度動作確認する（一括置換は事故のもと）
4. `.env` を .gitignore、`.env.example` をコミットする
5. 最後にもう一度 grep して取り残しゼロを確認する

## チェックリスト

- [ ] grep でポート/ホスト/機体名のハードコードが 0 件
- [ ] `.env.example` に全変数の例とコメントがある
- [ ] 機体固有・社外秘の値が `config/local/`（gitignore済み）にある
- [ ] `git check-ignore config/local .env` が通る
- [ ] README に「.env.example をコピーして開始」の記載がある
