# Third-party skills — provenance & review

`agents-config/` の全スキルはサードパーティ製。取り込み規約（`workflow/skill-creator` の「サードパーティ取り込み規約」）に従い、`SKILL.md` 全文をレビューし、`security/prompt-injection-scan` で走査（結果: HIGH/MEDIUM 0件）してから取り込んだ。install スクリプトは実行していない。

## claude-md-improver (Apache-2.0)

- Source: https://github.com/anthropics/claude-plugins-official — `plugins/claude-md-management/skills/claude-md-improver/`（公式 Anthropic プラグイン）
- License: Apache-2.0
- Reviewed: 2026-07-08. スクリプト・フック無し、全ファイル markdown、ネットワーク呼び出し無し、注入・隠し命令無し。
- Installed（verbatim）: `SKILL.md` + `references/{quality-criteria,templates,update-guidelines}.md`
- NOT installed: 同梱の `/revise-claude-md` コマンド（スラッシュコマンドでありスキルではないため）

## claude-md-drift-audit / claude-md-link-check / claude-md-dependency-rescan (MIT)

- Source: https://github.com/alirezarezvani/ClaudeForge — `skill/<name>/SKILL.md`
- License: MIT（Copyright (c) 2025 Alireza Rezvani）
- Reviewed: 2026-07-08. 3本はいずれも read-only（「never edits」を明示）・ローカルのみ・ネットワーク無し・注入無し。
- Installed（verbatim）: 上記3サブスキルの `SKILL.md` のみ
- NOT installed（意図的に除外）: 肥大な本体スキル `claude-md-enhancer`（約950行・haiku 固定・JSON I/F の非標準構成で claude-md-improver と重複）、`hooks/`・Python スクリプト群・`install.sh`/`install.ps1`・`command/`・`agent/`
