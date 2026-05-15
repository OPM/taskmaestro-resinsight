"""Task: Use an existing reservoir model."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import GridCase, LoadModelInput


class LoadModel(Task[LoadModelInput, GridCase]):
    """Pass an existing case through to downstream tasks."""

    name = "load_model"

    def run(self, input: LoadModelInput, ctx: ExecutionContext) -> GridCase:
        ctx.logger.info("Using existing case '%s'", input.case.value.name)
        return input.case
