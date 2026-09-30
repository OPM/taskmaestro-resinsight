"""Task: Configure the result and time step shown in a grid view."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import ConfigureGridViewInput, GridView


class ConfigureGridView(Task[ConfigureGridViewInput, GridView]):
    """Apply a cell result and time step to an existing grid view."""

    name = "configure_grid_view"

    def run(self, input: ConfigureGridViewInput, ctx: ExecutionContext) -> GridView:
        view = input.grid_view.value
        ctx.logger.info(
            "Configuring grid view with %s/%s at time step %d",
            input.result_type,
            input.result_variable,
            input.time_step,
        )
        view.apply_cell_result(  # type: ignore[attr-defined]
            result_type=input.result_type,
            result_variable=input.result_variable,
        )
        view.set_time_step(time_step=input.time_step)  # type: ignore[attr-defined]
        return input.grid_view
