"""Tests for SelectWellPath task."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.models import (
    GridCase,
    RipsInstance,
    SelectWellPathInput,
    WellPath,
)
from taskmaestro_resinsight.select_well_path import SelectWellPath


class TestSelectWellPath:
    def test_name(self) -> None:
        assert SelectWellPath.name == "select_well_path"

    def test_run_returns_input_well_path(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        loaded_grid_case: GridCase,
        loaded_well_path: WellPath,
    ) -> None:
        task = SelectWellPath()
        input_data = SelectWellPathInput(
            resinsight=rips_instance_model,
            grid_case=loaded_grid_case,
            well_path=loaded_well_path,
        )
        result = task.run(input_data, ctx)

        assert result is loaded_well_path
