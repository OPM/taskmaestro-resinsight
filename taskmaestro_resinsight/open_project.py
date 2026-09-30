"""Task: Open a ResInsight project from disk."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import OpenProjectInput, RipsInstance


class OpenProject(Task[OpenProjectInput, RipsInstance]):
    """Open a project file and pass through the ResInsight connection."""

    name = "open_project"

    def run(self, input: OpenProjectInput, ctx: ExecutionContext) -> RipsInstance:
        ctx.logger.info("Opening ResInsight project from '%s'", input.path)
        input.resinsight.value.project.open(input.path)
        ctx.logger.info("Opened ResInsight project")
        return input.resinsight
