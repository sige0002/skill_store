---
name: vla-policy-development
description: LeRobot 上で VLA（Vision-Language-Action）系ロボットポリシーを PyTorch で実装・改修するためのスキル。pi0/pi0.5 系ポリシーの派生実装、既存ポリシーの拡張、action normalization、policy config、データセット、学習ループ、評価スクリプト、シミュレーション（LIBERO 等）や実機デプロイに関わる作業で使用する。
---

# VLA Policy Development (LeRobot / PyTorch)

## Goal

LeRobot 上での VLA 系ロボットポリシー実装を支援する。既存ポリシー（pi0/pi0.5 など）から派生した新ポリシーの追加、PyTorch 移植、シミュレーション評価、実機デプロイまでを対象とする。

## Rules

- 既存コードベースが JAX 連携を要求しない限り、PyTorch ネイティブ実装を優先する
- LeRobot の既存の policy/config/dataset/training 構造に従う
- 最小限の拡張で済む場合、ポリシー全体を書き直さない
- LeRobotDataset、学習スクリプト、評価スクリプト、シミュレーションワークフローとの互換性を保つ
- 新ポリシーを追加する場合、上流のポリシー（例: `pi05`）を直接改変せず、`pi05_<variant>` のような別名で追加する
- 編集前に必ず既存のポリシー登録、config クラス、モデルクラス、processor/action normalization、学習エントリポイントを確認する

## Checklist（新しい派生ポリシーを実装するとき）

1. ベースとなる既存ポリシー実装を見つける
2. policy config、モデルクラス、前処理、action head、loss 関数、推論パスを特定する
3. 新ポリシー用のフォルダ/クラスを別名で作成する（上流を壊さない）
4. 変種固有のモジュールを、元のポリシーを壊さずに追加する
5. 変種固有の要素（loss、追加データ、conditioning、補助モデル等）は config フラグで切り替え可能にする
6. forward pass・loss 計算・action selection のテストまたはスモークスクリプトを追加する
7. 本格的な学習の前に、小さなシミュレーションデータセット（LIBERO 等）やダミーデータセットで検証する
8. 学習・評価・ベースポリシーとの比較方法をドキュメント化する

## Common failure points

- Action dimension mismatch（アクション次元の不一致）
- 正規化統計量（normalization statistics）の取り違え
- 画像/トークン系列の shape mismatch
- JAX/PyTorch チェックポイント前提の混在
- データセットのキー名とポリシー入力の不一致
- 自己回帰的 action decoding と連続 action head の混同
- 評価時と学習時で action scale が異なる
