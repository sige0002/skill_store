---
name: efficiency-review
description: 完了したタスクのワークフローを効率性の観点で振り返り、反復パターンと自動化機会を特定する。タスク完了後のレトロスペクティブ、改善提案、スキル化・フック化候補の発見に使用する。
allowed-tools: Read, Grep, Glob, Bash
---

# 効率レビュー

タスク完了後の効率レビューを実施し、最適化の機会を特定して今後のワークフローを改善する。

## 手順

### 1. 直近の作業を振り返る

```bash
git log --oneline -20
git diff --stat HEAD~5..HEAD 2>/dev/null || git diff --stat
git status
```

以下を把握する：どのファイルが変更されたか / コミット数 / 作業の全体的なゴール。

### 2. 反復パターンの特定

- git ログで類似のコミットメッセージが繰り返されていないか（複数の "fix lint" や "fix typo"）
- 同じファイルが複数コミットで変更されていないか（手戻りの兆候）
- 常にまとめて発生する変更の連鎖はないか（自動化候補）

```bash
# 最近のコミットで複数回変更されたファイルを見つける
git log --oneline --name-only -10 | sort | uniq -c | sort -rn | head -20
```

自問する：
- 2 回以上繰り返された手作業ステップはなかったか？
- 同じ情報を何度も参照する必要があった作業はなかったか？
- より良い事前チェックで防げた試行錯誤のサイクルはなかったか？

### 3. 自動化機会のチェック

手作業のステップを以下のいずれかに変換できないか評価する：

- **Git hooks**：pre-commit チェック、pre-push バリデーション
- **スキル**：再利用可能なワークフロー（skill-creator スキルで作成）
- **スクリプト**：複数ステップを扱うシェルスクリプトや Makefile

```bash
ls -la .git/hooks/ 2>/dev/null           # 既存フック
ls -la .claude/skills/ 2>/dev/null       # 既存スキル
ls Makefile .github/workflows/*.yml scripts/ 2>/dev/null
```

### 4. 改善度の測定

- 過去のアプローチを記録したメモリファイル（`~/.claude/projects/<project>/memory/`）を確認する
- コミット数、触れたファイル数、変更の複雑度などの指標を過去の類似作業と比較する
- 今回のアプローチで過去の問題を回避できたか？新しい問題は発生したか？

### 5. 結果レポート

```
## Efficiency Review Report

### Task Summary
- What was done / Files changed / Commits made

### Repetitive Patterns Found
- [pattern]: occurred [N] times, could be automated by [suggestion]

### Automation Opportunities
- [ ] Create a [hook/skill/script] to [description]

### Comparison to Previous Work
- Improved / Regressed / New issue

### Recommended Actions
1. [Most impactful action]
```

### 6. 必要なら CLAUDE.md を更新

今後のすべての作業に適用されるべき新パターンやルールが発見された場合、プロジェクトの `CLAUDE.md` に追記する。追加は最小限・実行可能に保ち、既存のルールは削除・改変しない。繰り返しのミスを確実に防ぐ、あるいは将来の作業を大幅に加速する、本当に有用なパターンだけを追加すること。ノイズは避ける。
