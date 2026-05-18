"""Task: Import a well path from disk."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import LoadWellPathInput, WellPath


class LoadWellPath(Task[LoadWellPathInput, WellPath]):
    """Import a well trajectory file (e.g. .dev) and wrap it as a WellPath."""

    name = "load_well_path"

    def run(self, input: LoadWellPathInput, ctx: ExecutionContext) -> WellPath:
        ctx.logger.info("Loading well path from '%s'", input.path)
        collection = input.resinsight.value.project.well_path_collection()
        wp = collection.import_well_path(file_name=input.path)
        ctx.logger.info("Loaded well path '%s'", wp.name)
        return WellPath(value=wp)
