"""Task: Use an existing well path."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import LoadWellPathInput, WellPath


class LoadWellPath(Task[LoadWellPathInput, WellPath]):
    """Pass an existing well path through to downstream tasks."""

    name = "load_well_path"

    def run(self, input: LoadWellPathInput, ctx: ExecutionContext) -> WellPath:
        ctx.logger.info("Using existing well path '%s'", input.well_path.value.name)
        return input.well_path
