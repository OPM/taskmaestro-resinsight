"""Task: Save the current ResInsight project."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import RipsInstance, SaveProjectInput


class SaveProject(Task[SaveProjectInput, RipsInstance]):
    """Save the current project and pass through the ResInsight connection."""

    name = "save_project"

    def run(self, input: SaveProjectInput, ctx: ExecutionContext) -> RipsInstance:
        destination = input.path or "the current project file"
        ctx.logger.info("Saving ResInsight project to %s", destination)
        input.resinsight.value.project.save(input.path)
        ctx.logger.info("Saved ResInsight project")
        return input.resinsight
