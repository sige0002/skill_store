---
name: modify-vlm
description: アーキテクチャ分析、コンポーネント特定、評価を伴って、Vision Language Model を安全に改修する。
---

# VLM 改修スキル

以下のリクエストに基づいて Vision Language Model を改修する：

**Request:** $ARGUMENTS

## ワークフロー

### Phase 1: モデルアーキテクチャ分析
変更前に **think hard** でモデルを理解する。

- モデルフレームワーク（HuggingFace Transformers、独自実装など）を特定する
- アーキテクチャをマップする：vision encoder、language model、projection レイヤ
- 画像入力からテキスト出力までの forward pass をトレースする
- config ファイル、モデルクラス定義、重みロードコードを特定する
- モデルサイズ、精度（fp16/bf16/fp32）、ハードウェア要件を記録する

### Phase 2: コンポーネント特定
- 変更対象のコンポーネントを特定する
- 各境界での入出力テンソル形状を理解する
- 凍結レイヤと学習可能レイヤを区別する
- attention mask、位置エンコーディング、特殊トークンを確認する
- 依存関係をマップする — このコンポーネントを変えると他に何が壊れるか

### Phase 3: バックアップと安全策
- 変更前にファイルをバックアップする：
  ```bash
  cp model.py model.py.bak
  ```
- 比較用に元のモデル出力を保存する（ゴールデンテスト）：
  ```python
  # Generate reference outputs before modification
  original_output = model.generate(test_input)
  torch.save(original_output, "reference_output.pt")
  ```

### Phase 4: 実装
- 対象コンポーネントを少しずつ改修する
- モジュール境界のテンソル形状を保つ — assertion を入れる：
  ```python
  assert hidden.shape == (batch, seq_len, hidden_dim), f"Shape mismatch: {hidden.shape}"
  ```
- attention 機構や loss 関数の変更には **think hard** を使う
- 変更は最小限にし、十分に文書化する

### Phase 5: 評価パイプライン
環境をセットアップする：
```bash
uv venv .venv && source .venv/bin/activate
uv pip install torch transformers pillow accelerate
```

評価を実行する：
- モデルがエラーなくロードできることを確認
- 参照入力に対する変更前後の出力を比較
- 可能なら標準 VLM ベンチマーク（VQA、キャプション生成など）を実行
- リグレッションを確認：BLEU、CIDEr、accuracy、タスク固有メトリクス

### Phase 6: 視覚的検証
- 多様な画像タイプ（写真、図、テキスト多めの画像）でテストする
- 画像前処理（resize、normalize）が正しいか確認する
- 視覚特徴量が言語空間に適切に射影されているか確認する
- 目視確認用のサンプル予測をログする

### Phase 7: サマリ
- 何を、なぜ変更したかを文書化する
- 変更前後のメトリクス比較をレポートする
- バックアップファイルの場所を列挙する
- 必要な設定変更を明示する

## ガイドライン
- モデル重みファイルを直接変更しない — チェックポイントではなくコードを変更する
- まず小さなバッチサイズでテストし、形状エラーを早期に捕まえる
- GPU メモリに注意 — `torch.cuda.max_memory_allocated()` で追跡する
- 評価時は `model.eval()` と `torch.no_grad()` を使う
