"""Tests for LoadModel task."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.models import GridCase, LoadModelInput, RipsInstance
from taskmaestro_resinsight.load_model import LoadModel


class TestLoadModel:
    def test_name(self) -> None:
        assert LoadModel.name == "load_model"

    def test_run_returns_input_case(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        loaded_grid_case: GridCase,
    ) -> None:
        task = LoadModel()
        input_data = LoadModelInput(
            resinsight=rips_instance_model,
            case=loaded_grid_case,
        )
        result = task.run(input_data, ctx)

        assert result is loaded_grid_case
