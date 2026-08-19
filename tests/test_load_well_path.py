"""Tests for LoadWellPath task (imports a well path from disk)."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.load_well_path import LoadWellPath
from taskmaestro_resinsight.models import (
    GridCase,
    LoadWellPathInput,
    RipsInstance,
    WellPath,
)


class TestLoadWellPath:
    def test_name(self) -> None:
        assert LoadWellPath.name == "load_well_path"

    def test_run_imports_well_path_from_path(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        loaded_grid_case: GridCase,
        well_path_a: str,
    ) -> None:
        task = LoadWellPath()
        input_data = LoadWellPathInput(
            resinsight=rips_instance_model,
            grid_case=loaded_grid_case,
            path=well_path_a,
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, WellPath)
        assert result.value is not None
        assert result.value.name
