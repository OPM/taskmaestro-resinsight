"""Task: Import a well path file into ResInsight."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from models import LoadWellPathInput, WellPath


class LoadWellPath(Task[LoadWellPathInput, WellPath]):
    """Import a well path file into ResInsight."""

    name = "load_well_path"

    def run(self, input: LoadWellPathInput, ctx: ExecutionContext) -> WellPath:
        instance = input.resinsight.value
        ctx.logger.info("Importing well path from %s", input.path)
        collection = instance.project.well_path_collection()
        well_path = collection.import_well_path(file_name=input.path)
        ctx.logger.info("Imported well path '%s'", well_path.name)
        return WellPath(value=well_path)
