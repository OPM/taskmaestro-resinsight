"""Task: Use an existing reservoir model."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import GridCase, SelectEclipseCaseInput


class SelectEclipseCase(Task[SelectEclipseCaseInput, GridCase]):
    """Pass an existing case through to downstream tasks."""

    name = "select_eclipse_case"

    def run(self, input: SelectEclipseCaseInput, ctx: ExecutionContext) -> GridCase:
        ctx.logger.info("Using existing case '%s'", input.case.value.name)
        return input.case
