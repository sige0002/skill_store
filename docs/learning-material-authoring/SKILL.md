---
name: learning-material-authoring
description: 技術トピックの初心者向け学習教材（日本語）を、章立て・演習・解答・ビルド可能なコード付きで作成するための型。「〜の学習教材を作って」「初心者向けのチュートリアルを書いて」「模擬問題も付けて」と言われたときに使用する。Typst/Marp によるPDF/スライド化、codex による教育レビューを含む。
---

# Learning Material Authoring（技術教材作成の型）

技術トピック（例: VLA、dora-rs、Isaac 等）について、完全初心者が手を動かして学べる教材を作るための定型構成。

## 教材の構成

```
<topic>-learn/
├── README.md            # 学習の進め方・前提・環境構築
├── book/                # 教材本文（章ごと）
│   ├── m0_setup.md      # M0: 環境構築
│   ├── m1_basics.md     # M1: 基礎概念
│   ├── ...              # M2..M6: 段階的に発展
│   └── answers/         # 演習の解答
├── src/                 # 教材で使う実行可能コード
├── exercises/           # 演習用の雛形コード
└── scripts/build_book.py  # PDF ビルド（Typst）
```

- **章立ては M0（環境構築）→ M6（総仕上げ）程度の段階構成**にし、各章は「本文 + 演習（模擬問題）+ 解答」をセットにする
- **実機・特殊ハードなしで完結**させる（シミュレーション/CPU で動く縮小版に置き換える）
- 想定読者を最初に固定する（例:「Python は書けるが対象分野は未経験」）

## コードの信頼性（最重要）

- 教材中のコード片は**すべて実行して検証**し、出力例には実測値を載せる（想像で書いた出力は初心者を最も混乱させる）
- 実行は `uv run`（依存グループは `--extra`）+ `PYTHONPATH=src` で統一し、README のコマンドをコピペすれば動く状態を保つ
- 依存は `pyproject.toml` に集約し、教材用 extra（例: `--extra book`）を分ける

## プレビュー/配布形式

- Markdown はプレビューが貧弱なので、配布用は **Typst で PDF 化**する:
  ```bash
  uv run --extra book python scripts/build_book.py   # md → typ → pdf
  ```
- スライドが必要な場合は Marp を使う（`marp slide.md -o slide.pdf`）
- 図は mermaid / 手書き SVG を md 側に置き、ビルドで埋め込む

## レビュー（2軸）

完成したら独立レビューを2軸で行う（codex-teammate スキル参照）:

1. **pedagogy レビュー** — 初心者がこの順で読んで詰まらないか、前提知識の飛躍がないか、演習の難易度勾配は適切か
2. **technical レビュー** — 技術的な誤り・古い API・動かないコードがないか

指摘はブラッシュアップして反映し、コードは再実行で確認する。

## 公開

教材は完成後 GitHub に public で公開する（github-publish スキル参照）。学習データや生成 PDF が大きい場合は gitignore し、ビルド手順を README に書く。
