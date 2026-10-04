"""Task: Create a modeled well path from well targets."""

from __future__ import annotations

import rips
from taskmaestro import ExecutionContext, Task

from .models import CreateWellPathInput, WellPath


class CreateWellPath(Task[CreateWellPathInput, WellPath]):
    """Create a modeled well path with targets relative to a reference point."""

    name = "create_well_path"

    def run(self, input: CreateWellPathInput, ctx: ExecutionContext) -> WellPath:
        collection = input.resinsight.value.project.well_path_collection()
        well_path = collection.add_new_object(rips.ModeledWellPath)
        well_path.name = input.name
        well_path.update()

        geometry = well_path.well_path_geometry()
        ref = input.reference_point
        geometry.reference_point = [ref.x, ref.y, ref.z]
        geometry.update()

        for target in input.targets:
            geometry.append_well_target([target.x, target.y, target.z])

        ctx.logger.info(
            "Created well path '%s' with %d targets", well_path.name, len(input.targets)
        )
        return WellPath(value=well_path)
