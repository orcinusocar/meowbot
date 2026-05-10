from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from meowbot.workspace import default_workspace_root


class Settings(BaseSettings):
    """从 config.json + 环境变量 MEOWBOT_* 读取；同名字段以构造参数为准（CLI 在 commands 里单独覆盖 workspace）。"""

    workspace_root: Optional[Path] = Field(
        default=None,
        description="工作目录；未设置则用 ~/.meowbot",
    )
    log_level: str = Field(default="INFO")
    # 接模型/提供商
    model_name: str = Field(default="", description="模型名")
    provider: str = Field(default="", description="提供商")

    model_config = SettingsConfigDict(
        env_prefix="MEOWBOT_",
        extra="ignore",
    )

    @classmethod
    def from_config_file(cls, path: Path) -> Settings:
        data: dict[str, Any] = {}
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)


def resolve_workspace_and_settings(cli_workspace: Optional[Path]) -> tuple[Path, Settings]:
    """
    确定实际 workspace 根目录与配置。
    优先级：CLI -w > config.json 中的 workspace_root > 默认 ~/.meowbot
    """
    default_root = default_workspace_root()

    if cli_workspace is not None:
        root = cli_workspace.expanduser().resolve()
        settings = Settings.from_config_file(root / "config.json")
        return root, settings

    boot = Settings.from_config_file(default_root / "config.json")
    if boot.workspace_root is not None:
        root = Path(boot.workspace_root).expanduser().resolve()
        cfg = root / "config.json"
        settings = Settings.from_config_file(cfg) if cfg.is_file() else boot
        return root, settings

    root = default_root
    settings = boot
    return root, settings
