"""Task: Close the current ResInsight project."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import RipsInstance


class CloseProject(Task[RipsInstance, RipsInstance]):
    """Close the current project and pass through the ResInsight connection."""

    name = "close_project"

    def run(self, input: RipsInstance, ctx: ExecutionContext) -> RipsInstance:
        ctx.logger.info("Closing the current ResInsight project")
        input.value.project.close()
        ctx.logger.info("Closed the ResInsight project")
        return input
