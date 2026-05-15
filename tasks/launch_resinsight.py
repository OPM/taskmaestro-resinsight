"""Task: Launch a ResInsight instance."""

from __future__ import annotations

import rips
from pydantic import BaseModel

from taskmaestro import ExecutionContext, Task

from models import RipsInstance


class LaunchResInsightInput(BaseModel):
    """Configuration for launching ResInsight."""

    resinsight_executable: str = ""
    console: bool = True


class LaunchResInsight(Task[LaunchResInsightInput, RipsInstance]):
    """Launch a new ResInsight instance."""

    name = "launch_resinsight"

    def run(self, input: LaunchResInsightInput, ctx: ExecutionContext) -> RipsInstance:
        ctx.logger.info("Launching ResInsight...")
        instance = rips.Instance.launch(
            resinsight_executable=input.resinsight_executable,
            console=input.console,
        )
        ctx.logger.info("Launched ResInsight on %s", instance.location)
        return RipsInstance(value=instance)
