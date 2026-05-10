from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from meowbot.logging_config import configure_logging
from meowbot.settings import resolve_workspace_and_settings
from meowbot.workspace import ensure_workspace


app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="meowbot: nanobot-style agent CLI scaffold.",
)


@app.callback()
def main(
    ctx: typer.Context,
    workspace: Annotated[
        Optional[Path],
        typer.Option(
            "--workspace",
            "-w",
            help="工作目录（覆盖 config.json 中的 workspace_root；默认 ~/.meowbot）",
            dir_okay=True,
            file_okay=False,
            resolve_path=True,
        ),
    ] = None,
) -> None:
    """
    meowbot 命令行入口。

    目前只提供最小子命令 `agent`（不接模型），后续会在这里继续挂更多能力。
    """
    ctx.ensure_object(dict)
    root, settings = resolve_workspace_and_settings(workspace)
    configure_logging(settings.log_level)
    ctx.obj["workspace"] = ensure_workspace(root)
    ctx.obj["settings"] = settings


@app.command()
def agent(
    ctx: typer.Context,
    message: Annotated[str, typer.Option("--message", "-m", help="要发送给 agent 的消息")],
) -> None:
    """
    最小 agent 命令：先只回显“收到消息”，不接模型。
    """

    ws = ctx.obj["workspace"]
    settings = ctx.obj["settings"]
    logger.info("workspace={}", str(ws.root))
    logger.info("sessions_dir={}", str(ws.sessions_dir))
    logger.info("config_file={}", str(ws.config_file))
    logger.debug("log_level={} provider={} model_name={}", settings.log_level, settings.provider, settings.model_name)
    typer.echo(f"收到消息：{message}")


if __name__ == "__main__":
    app()

