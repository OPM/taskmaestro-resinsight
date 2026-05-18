"""Task: Use an existing well path."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import SelectWellPathInput, WellPath


class SelectWellPath(Task[SelectWellPathInput, WellPath]):
    """Pass an existing well path through to downstream tasks."""

    name = "select_well_path"

    def run(self, input: SelectWellPathInput, ctx: ExecutionContext) -> WellPath:
        ctx.logger.info("Using existing well path '%s'", input.well_path.value.name)
        return input.well_path
