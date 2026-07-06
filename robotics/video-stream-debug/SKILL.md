---
name: video-stream-debug
description: WebRTC/MJPEG などのライブ映像プレビューが黒いまま・映らない・タブ切替後に固まるときのデバッグチェックリスト。「ライブプレビューが黒い」「ストリームが映らない」「カメラ映像が出ない」「タブを切り替えたら止まった」ときに使用する。
---

# Video Stream Debug（ライブ映像が映らないときのチェックリスト）

Web UI のライブ映像（WebRTC / MJPEG / SSE）が黒いまま・映らない問題は原因が多層（ブラウザ/codec/ネットワーク/配信元）にまたがる。**過去の事例で最も多かった真因はブラウザ差**なので、安価な確認から順に潰す。

## チェック順序（安価な順）

### 1. ブラウザを変える（最頻の真因）

**Firefox で WebRTC 映像が黒いまま → Chrome で映る**、という事例が複数プロジェクトで独立に再現している。コード側を疑う前に、まず Chrome/Chromium で開いて切り分ける。

- Chrome で映る → ブラウザ互換問題（codec/H.264 ライセンス/自動再生ポリシー）。UI に「推奨ブラウザ」を明記するか、MJPEG フォールバックを用意する
- Chrome でも黒い → 2 へ

### 2. 配信元にデータが来ているか確認

```bash
ros2 topic list                       # トピックが存在するか
ros2 topic hz /camera/image_raw       # 実際に流れているか（周波数）
ros2 topic echo /camera/... --once    # 中身が取れるか
```

- トピックが無い/止まっている → 配信側（bag play / ドライバ）の問題。rosbag-workflow スキル参照
- 流れているのに映らない → 3 へ

### 3. コンテナ間・プロセス間の疎通（DDS）

コンテナ内で `ros2 bag play` してトピックは流れているのにフロントに届かないケース：

- `ROS_DOMAIN_ID` が全コンテナ・ホストで一致しているか
- DDS 実装（CycloneDDS / FastDDS）が混在していないか（`RMW_IMPLEMENTATION` を統一）
- QoS 不一致（配信側 BEST_EFFORT vs 購読側 RELIABLE 等）で購読できていないか
- compose の `network_mode` / 共有メモリ設定（`/dev/shm`）が DDS の発見を妨げていないか

### 4. codec 非対応・変換失敗

- 「camera codec is unsupported by this browser」系のエラー → 別トピック（別エンコード）を選ぶ、またはサーバ側で再エンコードする
- compressed image topic の場合、バックエンドのデコードパスが対応フォーマットか確認する

### 5. タブ切替・再接続の問題

タブを離れて戻るとストリームが黒いまま（retry で直る）→ ブラウザがバックグラウンドタブのメディアを停止するため。対処：

- `visibilitychange` イベントで再接続をトリガーする
- 接続状態を監視し、フレームが N 秒来なければ自動 re-negotiate する
- 暫定対応としては UI に retry ボタンを用意する

## 予防策

- UI に接続状態・最終フレーム受信時刻・選択中 codec を表示するデバッグ表示を仕込む（黒画面の切り分けが一気に楽になる）
- 画像トピックをロボット外のネットワークに流すと帯域を圧迫し周波数が落ちる — プレビューは compressed topic か低解像度に絞る
