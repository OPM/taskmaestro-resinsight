"""Task: Import grid properties from disk."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import GridCase, ImportGridPropertyInput


class ImportGridProperty(Task[ImportGridPropertyInput, GridCase]):
    """Import grid property files into a loaded grid case."""

    name = "import_grid_property"

    def run(self, input: ImportGridPropertyInput, ctx: ExecutionContext) -> GridCase:
        ctx.logger.info("Loading grid properties from '%s'", input.paths)
        imported = input.grid_case.value.import_properties(file_names=input.paths)
        ctx.logger.info("Loaded grid properties: %s", imported.values)
        return GridCase(value=input.grid_case.value)
