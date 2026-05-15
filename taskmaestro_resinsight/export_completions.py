"""Task: Export completions (fan-in from multiple perforation branches)."""

from __future__ import annotations

import rips
from pydantic import BaseModel, ConfigDict

from taskmaestro import ExecutionContext, Task

from .models import GridCase, PerforationOutput, RipsInstance


class ExportCompletions(Task):  # type: ignore[type-arg]
    """Fan-in: merge case and perforations, then export completions.

    Uses inline Inputs/Outputs inner classes for the named-ports fan-in pattern.
    export_path comes from config.
    """

    name = "export_completions"

    class Inputs(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)

        resinsight: RipsInstance
        grid_case: GridCase
        perforation_1: PerforationOutput
        perforation_2: PerforationOutput
        event_date: str
        export_path: str

    class Outputs(BaseModel):
        export_file: str
        well_path_names: list[str]

    def run(self, input: Inputs, ctx: ExecutionContext) -> Outputs:
        eclipse_case = input.grid_case.value
        well_path_names = [
            input.perforation_1.value.name,
            input.perforation_2.value.name,
        ]
        ctx.logger.info(
            "Exporting completions for wells %s to %s",
            well_path_names,
            input.export_path,
        )

        instance = input.resinsight.value
        collection = instance.project.descendants(rips.WellPathCollection)[0]
        timeline = collection.event_timeline()
        timeline.set_timestamp(timestamp=input.event_date)

        eclipse_case.export_well_path_completions(
            time_step=0,
            well_path_names=well_path_names,
            file_split="UNIFIED_FILE",
            include_perforations=True,
            custom_file_name=input.export_path,
        )
        ctx.logger.info("Export complete: %s", input.export_path)
        return self.Outputs(
            export_file=input.export_path,
            well_path_names=well_path_names,
        )
