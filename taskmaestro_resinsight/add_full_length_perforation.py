"""Perforate a well path over its measured-depth range."""

from __future__ import annotations

import datetime
import math

from pydantic import BaseModel
from taskmaestro import ExecutionContext, Task

from .add_perforation import AddPerforation
from .models import AddPerforationInput, PerforationOutput, RipsInstance, WellPath


class AddFullLengthPerforationInput(BaseModel):
    resinsight: RipsInstance
    well_path: WellPath
    event_date: datetime.date


class AddFullLengthPerforation(Task[AddFullLengthPerforationInput, PerforationOutput]):
    """Create one event from the first to last MD of a well trajectory."""

    name = "add_full_length_perforation"

    def run(
        self, input: AddFullLengthPerforationInput, ctx: ExecutionContext
    ) -> PerforationOutput:
        depths = input.well_path.value.trajectory_properties(  # type: ignore[attr-defined]
            resampling_interval=10.0
        ).get("measured_depth", [])
        if len(depths) < 2 or not all(math.isfinite(md) for md in depths):
            raise ValueError(
                f"Well '{input.well_path.value.name}' has no valid MD range"
            )
        start_md, end_md = min(depths), max(depths)
        if end_md <= start_md:
            raise ValueError(
                f"Well '{input.well_path.value.name}' has no valid MD range"
            )
        return AddPerforation().run(
            AddPerforationInput(
                resinsight=input.resinsight,
                well_path=input.well_path,
                event_date=input.event_date,
                start_md=start_md,
                end_md=end_md,
            ),
            ctx,
        )


class AddFullLengthPerforationsInput(BaseModel):
    resinsight: RipsInstance
    well_paths: dict[str, WellPath]
    event_date: datetime.date


class FullLengthPerforations(BaseModel):
    perforations: dict[str, PerforationOutput]


class AddFullLengthPerforations(
    Task[AddFullLengthPerforationsInput, FullLengthPerforations]
):
    """Apply the single-well operation to a mapped load_wells output."""

    name = "add_full_length_perforations"

    def run(
        self, input: AddFullLengthPerforationsInput, ctx: ExecutionContext
    ) -> FullLengthPerforations:
        task = AddFullLengthPerforation()
        return FullLengthPerforations(
            perforations={
                key: task.run(
                    AddFullLengthPerforationInput(
                        resinsight=input.resinsight,
                        well_path=well,
                        event_date=input.event_date,
                    ),
                    ctx,
                )
                for key, well in input.well_paths.items()
            }
        )
