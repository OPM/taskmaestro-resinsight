"""Tests for LoadWellPath task."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.models import (
    GridCase,
    LoadWellPathInput,
    RipsInstance,
    WellPath,
)
from taskmaestro_resinsight.load_well_path import LoadWellPath


class TestLoadWellPath:
    def test_name(self) -> None:
        assert LoadWellPath.name == "load_well_path"

    def test_run_returns_input_well_path(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        loaded_grid_case: GridCase,
        loaded_well_path: WellPath,
    ) -> None:
        task = LoadWellPath()
        input_data = LoadWellPathInput(
            resinsight=rips_instance_model,
            grid_case=loaded_grid_case,
            well_path=loaded_well_path,
        )
        result = task.run(input_data, ctx)

        assert result is loaded_well_path
