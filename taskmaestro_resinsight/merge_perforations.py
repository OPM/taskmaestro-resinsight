"""Combine selected-well and mapped-well perforation outputs."""

from __future__ import annotations

from pydantic import BaseModel
from taskmaestro import ExecutionContext, Task

from .models import PerforationOutput


class MergePerforationsInput(BaseModel):
    selected: list[PerforationOutput]
    loaded: dict[str, PerforationOutput]


class MergedPerforations(BaseModel):
    perforations: list[PerforationOutput]


class MergePerforations(Task[MergePerforationsInput, MergedPerforations]):
    """Flatten mapped results into the collected list, preserving input order."""

    name = "merge_perforations"

    def run(
        self, input: MergePerforationsInput, ctx: ExecutionContext
    ) -> MergedPerforations:
        return MergedPerforations(
            perforations=[*input.selected, *input.loaded.values()]
        )
