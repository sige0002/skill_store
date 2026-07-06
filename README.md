# skill_store

Claude Code 用スキルの個人ストア。各プロジェクト（`~/.claude/skills`、各リポジトリの `.claude/skills` 等）に散在していたスキルをカテゴリ別に集約し、類似スキルを統合・プロジェクト固有スキルを汎化したもの。加えて、過去の Claude Code 会話履歴（11プロジェクト・約52セッション）を分析し、繰り返し行っていた作業をスキル化して収録している。

## 使い方

必要なスキルをプロジェクトへコピー（またはシンボリックリンク）する：

```bash
# プロジェクト固有に入れる
cp -r <category>/<skill-name> /path/to/project/.claude/skills/

# 全プロジェクト共通で使う
cp -r <category>/<skill-name> ~/.claude/skills/
```

## スキル一覧

### coding/ — 開発ワークフロー

| スキル | 内容 |
|---|---|
| [tdd-python](coding/tdd-python/SKILL.md) | TDD で Python モジュールを実装する標準手順。SQLite（FTS5/Upsert）パターンは references/ に収録 |
| [implement-algorithm](coding/implement-algorithm/SKILL.md) | 研究論文のアルゴリズムをテスト・ベンチマーク付きで実装する |
| [implement-app](coding/implement-app/SKILL.md) | 要件分析→設計→実装→テスト→検証のアプリ開発ワークフロー |
| [modify-oss](coding/modify-oss/SKILL.md) | プロジェクト規約に従った OSS 改修と PR 準備 |
| [layered-config](coding/layered-config/SKILL.md) | ポート/ホスト/機体名のハードコード排除と .env + 3層 config への外部化 |

### docs/ — ドキュメント・教材

| スキル | 内容 |
|---|---|
| [sync-docs](docs/sync-docs/SKILL.md) | 日本語ドキュメント（正本）から英語ミラーを一方向再生成して同期する |
| [learning-material-authoring](docs/learning-material-authoring/SKILL.md) | 初心者向け技術教材（章立て＋演習＋解答＋検証済みコード＋Typst/Marp ビルド）作成の型 |

### git/ — Git / GitHub 運用

| スキル | 内容 |
|---|---|
| [github-publish](git/github-publish/SKILL.md) | リポジトリの GitHub 公開手順。機密スキャン・大容量データ除外・著者ポリシーを含む |
| [branch-cleanup](git/branch-cleanup/SKILL.md) | 作業ブランチの統合・マージ済み削除・fork の upstream 整理 |

### ml/ — 機械学習モデル

| スキル | 内容 |
|---|---|
| [modify-vlm](ml/modify-vlm/SKILL.md) | Vision Language Model の安全な改修（アーキテクチャ分析・ゴールデンテスト・評価） |
| [vla-policy-development](ml/vla-policy-development/SKILL.md) | LeRobot 上での VLA ポリシー実装・派生ポリシー追加（PyTorch） |

### robotics/ — ロボティクス / ROS 2

| スキル | 内容 |
|---|---|
| [ros2-development](robotics/ros2-development/SKILL.md)* | rclpy/rclcpp、QoS、DDS、colcon の ROS 2 開発ベストプラクティス |
| [ros2-web-integration](robotics/ros2-web-integration/SKILL.md)* | FastAPI+rclpy ブリッジ、WebSocket/SSE/MJPEG/WebRTC 連携 |
| [docker-ros2-development](robotics/docker-ros2-development/SKILL.md)* | ROS 2 の Docker 開発（マルチステージ、compose、コンテナ間 DDS、GPU） |
| [robotics-testing](robotics/robotics-testing/SKILL.md)* | ロボットソフトのテスト（pytest、launch_testing、mock HW、golden-file） |
| [robotics-software-principles](robotics/robotics-software-principles/SKILL.md)* | ロボットソフト設計原則（SOLID、プラグイン構成、config-over-code） |
| [lerobot-robot-integration](robotics/lerobot-robot-integration/SKILL.md) | LeRobot への新規ロボット（実機ドライバ）追加テンプレート |
| [rosbag-workflow](robotics/rosbag-workflow/SKILL.md) | rosbag の記録・ループ再生テストと DDS/QoS トラブル切り分け |
| [rosbag-to-lerobot](robotics/rosbag-to-lerobot/SKILL.md) | rosbag(mcap) → LeRobot データセット変換の手順と落とし穴集 |
| [video-stream-debug](robotics/video-stream-debug/SKILL.md) | ライブ映像プレビューが黒い/映らないときのデバッグチェックリスト |

\* 印はサードパーティ製スキル（Apache-2.0）。出典とレビュー記録は [robotics/SOURCES.md](robotics/SOURCES.md) を参照。

### security/ — セキュリティ

| スキル | 内容 |
|---|---|
| [dependency-audit](security/dependency-audit/SKILL.md) | 依存パッケージのセキュリティ監査（インストール前クイック監査 + サプライチェーン詳細レビュー） |

### workflow/ — メタワークフロー

| スキル | 内容 |
|---|---|
| [multi-agent-coordination](workflow/multi-agent-coordination/SKILL.md) | マルチエージェント並列開発の協調パターン（フェーズ設計・衝突回避・敵対的レビュー編成） |
| [codex-teammate](workflow/codex-teammate/SKILL.md) | codex CLI を第2意見レビュアーとして使う定型手順 |
| [skill-creator](workflow/skill-creator/SKILL.md) | スキルの作成・改修・統合とパターンのメモリ保存、サードパーティ取込規約 |
| [efficiency-review](workflow/efficiency-review/SKILL.md) | タスク完了後の効率レビューと自動化機会の特定 |
| [issue-log](workflow/issue-log/SKILL.md) | 遭遇した問題と解決策を簡潔に蓄積するローカル知識ベース |

## 統合・汎化の記録

- `tdd-python` ← `tdd-python-module` + `sqlite-tdd-pattern` を統合
- `dependency-audit` ← `audit-install` + `security-check` を統合
- `multi-agent-coordination` ← `parallel-agent-coordination` + `coordinate-team` を統合し、会話履歴から実績のあるチーム編成テンプレを追記
- `skill-creator` ← `workspace-skill-creator` + `save-workflow` を統合
- `vla-policy-development` ← `lerobot-vla-pytorch` を汎化（特定の派生ポリシー固有の記述を一般化）
- `lerobot-robot-integration` ← `lerobot-robot-config` を汎化（特定機体への参照を除去）
- `codex-teammate` / `github-publish` / `branch-cleanup` / `layered-config` / `video-stream-debug` / `rosbag-workflow` / `rosbag-to-lerobot` / `learning-material-authoring` は会話履歴の頻出パターン分析から新規作成

## ライセンス

- `robotics/` の * 印5スキル: Apache-2.0（[出典](https://github.com/arpitg1304/robotics-agent-skills)、詳細は robotics/SOURCES.md）
- その他: 本リポジトリのオリジナル
