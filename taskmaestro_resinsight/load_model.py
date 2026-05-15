"""Task: Load a reservoir model (.egrid) into ResInsight."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from models import GridCase, LoadModelInput


class LoadModel(Task[LoadModelInput, GridCase]):
    """Load the reservoir model (.egrid) into ResInsight."""

    name = "load_model"

    def run(self, input: LoadModelInput, ctx: ExecutionContext) -> GridCase:
        ctx.logger.info("Loading model from %s", input.path)
        grid_case = input.resinsight.value.project.load_case(input.path)
        ctx.logger.info("Loaded case '%s' (id=%d)", grid_case.name, grid_case.id)
        return GridCase(value=grid_case)
