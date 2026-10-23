"""Task: Export completions (fan-in from multiple perforation branches)."""

from __future__ import annotations

import datetime
import pathlib

import rips
from pydantic import BaseModel, ConfigDict, Field
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
        event_date: datetime.date = Field(description="Perforation event date")
        export_path: pathlib.Path = Field(
            description="Path to write the completions file"
        )

    class Outputs(BaseModel):
        export_file: str
        well_path_names: list[str]

    def run(self, input: Inputs, ctx: ExecutionContext) -> Outputs:
        return self._export(
            input.resinsight,
            input.grid_case,
            [input.perforation_1.value.name, input.perforation_2.value.name],
            input.event_date,
            input.export_path,
            ctx,
        )

    def _export(
        self,
        resinsight: RipsInstance,
        grid_case: GridCase,
        well_path_names: list[str],
        event_date: datetime.date,
        export_path: pathlib.Path,
        ctx: ExecutionContext,
    ) -> Outputs:
        eclipse_case = grid_case.value
        ctx.logger.info(
            "Exporting completions for wells %s to %s",
            well_path_names,
            export_path,
        )

        instance = resinsight.value
        collection = instance.project.descendants(rips.WellPathCollection)[0]
        timeline = collection.event_timeline()
        timeline.set_timestamp(timestamp=event_date)

        eclipse_case.export_well_path_completions(
            time_step=0,
            well_path_names=well_path_names,
            file_split="UNIFIED_FILE",
            include_perforations=True,
            custom_file_name=str(export_path),
        )
        ctx.logger.info("Export complete: %s", export_path)
        return self.Outputs(
            export_file=str(export_path),
            well_path_names=well_path_names,
        )


class ExportCollectedCompletions(ExportCompletions):
    """Export collected perforations on selected and dynamically loaded wells."""

    name = "export_collected_completions"

    class Inputs(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)

        resinsight: RipsInstance
        grid_case: GridCase
        perforations: list[PerforationOutput]
        event_date: datetime.date
        export_path: pathlib.Path

    def run(self, input: Inputs, ctx: ExecutionContext) -> ExportCompletions.Outputs:  # type: ignore[override]
        # Keep insertion order while avoiding duplicate well names.
        names = list(dict.fromkeys(perf.value.name for perf in input.perforations))
        return self._export(
            input.resinsight,
            input.grid_case,
            names,
            input.event_date,
            input.export_path,
            ctx,
        )
