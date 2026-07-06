---
name: lerobot-robot-integration
description: LeRobot に新しいロボット（実機ドライバ）を追加するためのテンプレートと手順。RobotConfig/Robot クラスの実装、observation/action features の定義、カメラ統合、双腕構成、utils.py への登録が必要なときに使用する。
---

# LeRobot Robot Integration ガイド

LeRobot に新しいロボットを追加するための手順テンプレート。`lerobot/src/lerobot/robots/` 配下の既存実装（単腕・双腕）を参考にする。

## 1. ファイル構成

```
lerobot/src/lerobot/robots/my_robot/
├── __init__.py           # ConfigとRobotクラスをエクスポート
├── config_my_robot.py    # @RobotConfig.register_subclass デコレータ付きConfig
└── my_robot.py           # Robot基底クラスの実装
```

## 2. `config_my_robot.py` テンプレート

```python
from dataclasses import dataclass, field

from lerobot.cameras import CameraConfig
from ..config import RobotConfig


@RobotConfig.register_subclass("my_robot")   # ← utils.py の type 文字列と一致させる
@dataclass
class MyRobotConfig(RobotConfig):
    """My robot configuration."""

    # id は RobotConfig から継承（デフォルト None）。必要に応じて上書き
    id: str | None = "default"

    # ロボット固有パラメータ（例）
    ip: str = "192.168.1.100"
    port: int = 8080
    velocity: int = 30

    # カメラ設定（必須フィールド）
    cameras: dict[str, CameraConfig] = field(default_factory=dict)
```

**ポイント:**
- `@RobotConfig.register_subclass("my_robot")` の文字列が `config.type` として使われる
- `@dataclass` は `@register_subclass` の**内側**（下側）に置く
- `cameras` フィールドは必ず `field(default_factory=dict)` で定義する
- `id` は `RobotConfig` が持つが、具体的なデフォルト値を設定する場合は上書きする

## 3. `my_robot.py` テンプレート

```python
import logging
from functools import cached_property

from lerobot.cameras.utils import make_cameras_from_configs
from lerobot.processor import RobotAction, RobotObservation
from lerobot.utils.decorators import check_if_already_connected, check_if_not_connected

from ..robot import Robot
from .config_my_robot import MyRobotConfig

logger = logging.getLogger(__name__)


class MyRobot(Robot):
    """My robot implementation."""

    config_class = MyRobotConfig   # ← 必須クラス変数
    name = "my_robot"              # ← 必須クラス変数

    def __init__(self, config: MyRobotConfig):
        super().__init__(config)
        self.config = config
        self.cameras = make_cameras_from_configs(config.cameras)  # カメラ初期化
        self._is_connected = False

    # --- features（observation/actionの型定義）---

    @cached_property
    def observation_features(self) -> dict[str, type | tuple]:
        """観測空間の定義: モータ位置 + カメラ画像"""
        motors = {"joint_1.pos": float, "joint_2.pos": float}  # 例
        cameras = {
            cam_key: (cfg.height, cfg.width, 3)
            for cam_key, cfg in self.config.cameras.items()
        }
        return {**motors, **cameras}

    @cached_property
    def action_features(self) -> dict[str, type]:
        """アクション空間の定義: モータ位置のみ"""
        return {"joint_1.pos": float, "joint_2.pos": float}  # 例

    # --- 状態プロパティ ---

    @property
    def is_connected(self) -> bool:
        return self._is_connected and all(cam.is_connected for cam in self.cameras.values())

    @property
    def is_calibrated(self) -> bool:
        return True  # アブソリュートエンコーダの場合は True 固定

    def calibrate(self) -> None:
        pass  # キャリブレーション不要の場合は pass

    # --- 接続・設定 ---

    @check_if_already_connected
    def connect(self, calibrate: bool = True) -> None:
        """ロボットとカメラに接続する。"""
        # ロボット接続処理
        # ...
        for cam in self.cameras.values():
            cam.connect()
        self._is_connected = True
        self.configure()
        logger.info(f"{self} connected.")

    def configure(self) -> None:
        """接続後の初期設定（初期姿勢への移動など）。"""
        pass

    # --- 観測・アクション ---

    @check_if_not_connected
    def get_observation(self) -> RobotObservation:
        """現在の関節角度とカメラ画像を返す。"""
        obs = {}
        # 関節状態の読み取り
        # obs["joint_1.pos"] = ...
        # カメラ画像の読み取り
        for cam_key, cam in self.cameras.items():
            obs[cam_key] = cam.read_latest()
        return obs

    @check_if_not_connected
    def send_action(self, action: RobotAction) -> RobotAction:
        """関節位置コマンドをロボットに送る。"""
        # action["joint_1.pos"] などを取り出して送信
        # ...
        return action

    def disconnect(self) -> None:
        """切断処理（どの状態から呼ばれても安全に動作すること）。"""
        for cam in self.cameras.values():
            cam.disconnect()
        self._is_connected = False
        logger.info(f"{self} disconnected.")
```

**実装必須メソッド一覧:**

| メソッド | 説明 |
|---|---|
| `observation_features` | 観測空間の型定義 (property) |
| `action_features` | アクション空間の型定義 (property) |
| `is_connected` | 接続状態 (property) |
| `is_calibrated` | キャリブレーション状態 (property) |
| `connect()` | ロボット・カメラへの接続 |
| `calibrate()` | キャリブレーション（不要なら pass） |
| `configure()` | 接続後の初期設定 |
| `get_observation()` | 観測値の取得 |
| `send_action()` | アクション送信 |
| `disconnect()` | 切断処理 |

## 4. `__init__.py` テンプレート

```python
from .config_my_robot import MyRobotConfig
from .my_robot import MyRobot
```

## 5. `robots/utils.py` への登録

`lerobot/src/lerobot/robots/utils.py` の `make_robot_from_config()` 関数に `elif` 分岐を追加する:

```python
elif config.type == "my_robot":
    from .my_robot import MyRobot

    return MyRobot(config)
```

既存の分岐の並びに合わせて追加する。

## 6. 使用スクリプトへのインポート追加（オプション）

スクリプト側でロボットモジュールを明示的に登録する場合:

```python
from lerobot.robots import my_robot  # noqa: F401
```

`noqa: F401` は「未使用インポート」の lint 警告を抑制するために必要。

## 7. 双腕ロボット（bi_robot）の場合の注意点

双腕構成では左右の腕を別々に接続・制御する:

- Config: `ip_left`, `ip_right` など左右別パラメータを定義する
- `joint_names` は片腕分のみ定義し、実行時に `left_` / `right_` プレフィックスを付与する
- `observation_features` / `action_features` で左右のキーを展開する

**キー名の注意:** データセット側のキー名（例: `right_arm_joint_1_rad`）とロボット実装側のキー名（例: `right_joint_1.pos`）が異なる場合、デプロイ時にリネームマッピングが必要。

## 8. 環境構築

lerobot は `uv pip install -e lerobot/` で正しくインストールすること。
これにより `lerobot-train`, `lerobot-calibrate` 等の CLI コマンドが使える。

```bash
uv venv .lerobot_venv --python 3.12
uv pip install -e lerobot/ --python .lerobot_venv/bin/python
```

aarch64 (Jetson) では torchcodec が自動除外され、pyav backend にフォールバックする。
torchvision が正しくインストールされていれば VideoReader 経由で動画デコードが動作する。

## 9. 参考実装

- 単腕・双腕の既存実装: `lerobot/src/lerobot/robots/` 配下の各ロボットフォルダ
- 登録先: `lerobot/src/lerobot/robots/utils.py`
- RobotConfig基底クラス: `lerobot/src/lerobot/robots/config.py`
- Robot基底クラス: `lerobot/src/lerobot/robots/robot.py`
