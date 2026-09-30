"""Task: Exit a ResInsight application instance."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import ExitResult, RipsInstance


class ExitResInsight(Task[RipsInstance, ExitResult]):
    """Send the exit command to a ResInsight application instance."""

    name = "exit_resinsight"

    def run(self, input: RipsInstance, ctx: ExecutionContext) -> ExitResult:
        ctx.logger.info("Exiting ResInsight")
        input.value.exit()
        ctx.logger.info("Sent the ResInsight exit command")
        return ExitResult(exited=True)
