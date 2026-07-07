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

### agents-config/ — CLAUDE.md / AGENTS.md 運用

| スキル | 内容 |
|---|---|
| [claude-md-improver](agents-config/claude-md-improver/SKILL.md)† | CLAUDE.md を6基準ルーブリックで採点し、最小差分で改善提案（公式 Anthropic・全ファイル markdown） |
| [claude-md-drift-audit](agents-config/claude-md-drift-audit/SKILL.md)† | git 履歴と CLAUDE.md の乖離（ドリフト）を read-only で検出 |
| [claude-md-link-check](agents-config/claude-md-link-check/SKILL.md)† | CLAUDE.md の @import・markdown リンク切れを read-only で検証 |
| [claude-md-dependency-rescan](agents-config/claude-md-dependency-rescan/SKILL.md)† | 依存マニフェストと CLAUDE.md の差分を read-only で検出 |

† 印はサードパーティ製スキル。出典・ライセンス（Apache-2.0 / MIT）・レビュー記録は [agents-config/SOURCES.md](agents-config/SOURCES.md) を参照。

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
| [urdf-mjcf-to-usd-conversion](robotics/urdf-mjcf-to-usd-conversion/SKILL.md)* | URDF/MJCF → USD 変換パイプライン（Isaac Sim / Lab、xacro 対応） |
| [isaac-sim-ros2-bridge](robotics/isaac-sim-ros2-bridge/SKILL.md)* | Isaac Sim ↔ ROS 2 ブリッジ（OmniGraph、Nav2、namespacing） |
| [physics-simulation](robotics/physics-simulation/SKILL.md)* | Isaac Sim の物理シーン構成・physics センサ（例集付き） |
| [data-collection-sim](robotics/data-collection-sim/SKILL.md)* | Replicator による合成データ生成（VLA/LeRobot 学習データ） |
| [isaac-sim-troubleshooting](robotics/isaac-sim-troubleshooting/SKILL.md)* | Isaac Sim の診断フローチャート |
| [usd-articulation](robotics/usd-articulation/SKILL.md)* | マルチアーム robot articulation の USD 構築・検証（Robot Schema） |
| [isaac-sim-sensor](robotics/isaac-sim-sensor/SKILL.md)* | RTX/physics センサ・ベンダ lidar/radar・Replicator ランダム化 |
| [navigation-primitives](robotics/navigation-primitives/SKILL.md)* | 移動ロボットナビの共通基盤（OccupancyMap、A*、footprint、chase camera） |
| [occupancy-map](robotics/occupancy-map/SKILL.md)* | USD シーン → ROS 占有格子マップ生成（Nav2/MobilityGen 連携） |
| [ros2-engineering-skills](robotics/ros2-engineering-skills/SKILL.md)* | ROS 2 開発の広範リファレンス（micro-ROS/PREEMPT_RT/MoveIt2/SROS2/Open-RMF/sim2real）。ros2-development の補完 |

\* 印はサードパーティ製スキル。出典・ライセンス・レビュー記録は [robotics/SOURCES.md](robotics/SOURCES.md) を参照。arpitg1304 由来の5スキルと IsaacSim 9スキルは Apache-2.0（verbatim）。`ros2-engineering-skills` は Apache-2.0（frontmatter の hooks/evals を除去した改変あり）。

### security/ — セキュリティ

| スキル | 内容 |
|---|---|
| [dependency-audit](security/dependency-audit/SKILL.md) | 依存パッケージのセキュリティ監査（インストール前クイック監査 + サプライチェーン詳細レビュー） |
| [prompt-injection-scan](security/prompt-injection-scan/SKILL.md) | 外部スキル取込前に SKILL.md/AGENTS.md/CLAUDE.md をプロンプトインジェクション・脱獄・秘密送信・不可視文字の観点で走査（7分類パターン＋実行コード同梱検知） |

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

- `robotics/` の * 印スキル: サードパーティ製。arpitg1304 由来5スキルと IsaacSim 9スキルは Apache-2.0（verbatim）、`ros2-engineering-skills` は Apache-2.0（改変あり）。詳細は [robotics/SOURCES.md](robotics/SOURCES.md)
- `agents-config/` の † 印スキル: サードパーティ製（Apache-2.0 / MIT）。詳細は [agents-config/SOURCES.md](agents-config/SOURCES.md)
- その他: 本リポジトリのオリジナル
