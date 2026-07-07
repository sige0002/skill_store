# Third-party skills — provenance & review

The following skills in this directory are third-party (installed verbatim; every `SKILL.md` reviewed, **no `scripts/` present** in any):

- Source: https://github.com/arpitg1304/robotics-agent-skills (Apache-2.0, ~289★)
- Reviewed: 2026-06-24. Security scan: markdown-only, no executable code; content is robotics best-practice reference. `install.sh` (benign copy script) was reviewed but NOT run — skills copied manually.

Installed:
- `ros2-development`            (repo `skills/ros2`)            — rclpy/rclcpp, QoS, DDS, colcon, components
- `ros2-web-integration`        (repo `skills/ros2-web-integration`) — FastAPI+rclpy bridge, WebSocket/SSE/MJPEG/WebRTC, CORS
- `docker-ros2-development`     (repo `skills/docker-ros2-development`) — multi-stage Dockerfiles, compose, cross-container DDS, GPU
- `robotics-testing`            (repo `skills/robotics-testing`) — pytest, launch_testing, mock HW, golden-file, deterministic
- `robotics-software-principles`(repo `skills/robotics-software-principles`) — SOLID, plugin arch, config-over-code

Reviewed but NOT installed (off-scope): `ros1`, `robot-perception`, `robotics-design-patterns`, `robotics-security`, `robot-bringup`.
Not installed (marketplace-only — scripts unverifiable, or redundant with built-in /code-review): skills.rest `ros2-skill`, `awesome-skills/code-review-skill`, `harunkurtdev/ros2-claude-code-template` (no license).

Apache-2.0 applies to the five skills above; see the source repo's LICENSE.

`lerobot-robot-integration` is NOT from this source — it is an original skill in this repository.

---

## 追加取込 (2026-07-08)

以下も別ソースのサードパーティ。取り込み規約に従い `SKILL.md` 全文をレビューし、`security/prompt-injection-scan` で走査（新規取込分すべて HIGH/MEDIUM 0件）してから取り込んだ。install スクリプトは実行していない。

### IsaacSim シミュレーション系 9スキル (Apache-2.0)

- Source: https://github.com/isaac-sim/IsaacSim — `skills/<name>/`（公式 NVIDIA リポジトリ, ~3.6k★）
- License: Apache-2.0（リポジトリ LICENSE）。※ Isaac Sim 本体（Omniverse Kit SDK・3D アセット）の実行/ビルドには別途 NVIDIA ライセンスが必要だが、この `skills/` の markdown ドキュメント配布には及ばない。
- Reviewed: 2026-07-08。全スキルの `SKILL.md` 本文を精読、注入・隠し命令・base64・curl-pipe・外部送信は無し。挙動を指示するのはリポジトリ直下の `AGENTS.md` / `SKILLS.md` のみで、これらは**取り込んでいない**（per-skill の `SKILL.md` だけを取得）。
- Installed（verbatim）:
  - `urdf-mjcf-to-usd-conversion/SKILL.md` — URDF/MJCF → USD 変換パイプライン
  - `isaac-sim-ros2-bridge/SKILL.md` — Isaac↔ROS2 ブリッジ（OmniGraph/Nav2/namespacing）※SKILL.md のみ。本文が参照する `scripts/`（2本）は取り込まず、参照マーカーが残る
  - `physics-simulation/SKILL.md` + `examples.md` — 物理シーン構成・physics センサ
  - `data-collection-sim/SKILL.md` — Replicator による合成データ生成（VLA/LeRobot 学習用）※SKILL.md のみ。同梱 `scripts/`（2本）は取り込まず（本文はスクリプト非依存で自己完結）
  - `isaac-sim-troubleshooting/SKILL.md` — 診断フローチャート
  - `usd-articulation/SKILL.md` — マルチアーム articulation の構築・検証
  - `isaac-sim-sensor/SKILL.md` — RTX/physics センサ・ベンダ lidar・Replicator
  - `navigation-primitives/SKILL.md` — 移動ロボットナビの共通基盤（OccupancyMap/A*/footprint）
  - `occupancy-map/SKILL.md` — USD シーン → ROS 占有格子マップ生成
- NOT installed: 上記2スキルの `scripts/`、および repo 直下の `AGENTS.md`/`SKILLS.md`、script-heavy な repo 内製ツール（isaac-sim-remote/orchestrator/validator/profile 等）とメタスキル（meta-skills/skill-distillation）。

### ros2-engineering-skills (Apache-2.0) — **改変あり**

- Source: https://github.com/dbwls99706/ros2-engineering-skills — ルートの `SKILL.md`
- License: Apache-2.0（Copyright 2025 dbwls99706）
- Reviewed: 2026-07-08。本文は自己完結。同梱の PreToolUse/Stop フック 2本（`skill_validate_hook.py` / `skill_stop_hook.py`）は fable 評価で全文監査済み・ネットワーク/eval/exfil 無しと確認したが、本ストアの方針（実行コードは持ち込まない）により**除外**。
- Installed: `SKILL.md` のみ。**改変**: frontmatter の `hooks:`（存在しないスクリプトを python3 実行するステンザ）と `evals:`（存在しない eval ファイルを参照するステンザ）を削除した。両者は取り込まなかったファイルを指すため、残すとエラー要因になる。verbatim ではない点をここに明記する。
- NOT installed: `scripts/`（7本）、`references/`（~20本）、`docs/`、`.claude-plugin/`。
- 既存 `ros2-development`（arpitg1304 由来）と話題が重複するが、micro-ROS/PREEMPT_RT/MoveIt2/SROS2/Open-RMF/sim2real まで**より広範**なため、置換ではなく**補完（別スキル）**として追加（ユーザー判断 2026-07-08）。

### 見送り（このバッチで採用しなかったもの）

- `adityakamath/ros2-skill`（Apache-2.0）— 実機ランタイム制御アプリ。SKILL.md 単体では機能せず、700KB の未監査 Python に依存。`scripts/discord_tools.py` が bot トークンを平文設定から読んで画像を Discord へ POST する外部送信経路を持つため見送り。
- `OpenRAL/openral` rskills（Apache-2.0）— `SKILL.md` は `rskill.yaml` の自動生成ミラーで、専用ランタイム無しでは単体価値が無い。プロジェクトも作成3週間・1★と未成熟のため見送り。
- `netresearch/agent-rules-skill`（MIT + **CC-BY-SA-4.0**）— AGENTS.md 生成器として最良だが、content のシェアアライク義務を public リポジトリに持ち込む点と、29 スクリプト中 24 本未監査のため見送り（ユーザー判断 2026-07-08）。

