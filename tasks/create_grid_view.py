"""Task: Create a new grid view on a loaded Eclipse case."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from models import GridCase, GridView


class CreateGridView(Task[GridCase, GridView]):
    """Create a new grid view on the loaded Eclipse case."""

    name = "create_grid_view"

    def run(self, input: GridCase, ctx: ExecutionContext) -> GridView:
        ctx.logger.info("Creating a grid view for case '%s'", input.value.name)
        view = input.value.create_view()
        ctx.logger.info("Created grid view")
        return GridView(value=view)
