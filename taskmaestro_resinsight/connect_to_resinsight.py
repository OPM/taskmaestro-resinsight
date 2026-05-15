"""Task: Connect to a running ResInsight instance."""

from __future__ import annotations

import rips

from taskmaestro import EmptyConfig, ExecutionContext, Task

from models import RipsInstance


class ConnectToResInsight(Task[EmptyConfig, RipsInstance]):
    """Connect to a running ResInsight instance."""

    name = "connect_to_resinsight"

    def run(self, input: EmptyConfig, ctx: ExecutionContext) -> RipsInstance:
        ctx.logger.info("Connecting to ResInsight...")
        instance = rips.Instance.find()
        ctx.logger.info("Connected to ResInsight on %s", instance.location)
        return RipsInstance(value=instance)
