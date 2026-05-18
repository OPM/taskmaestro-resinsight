"""Task: Load a reservoir model from disk."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import GridCase, LoadModelInput


class LoadModel(Task[LoadModelInput, GridCase]):
    """Open an Eclipse case from a file path and wrap it as a GridCase."""

    name = "load_model"

    def run(self, input: LoadModelInput, ctx: ExecutionContext) -> GridCase:
        ctx.logger.info("Loading case from '%s'", input.path)
        case = input.resinsight.value.project.load_case(input.path)
        ctx.logger.info("Loaded case '%s'", case.name)
        return GridCase(value=case)
