"""Tests for SelectEclipseCase task."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.models import GridCase, RipsInstance, SelectEclipseCaseInput
from taskmaestro_resinsight.select_eclipse_case import SelectEclipseCase


class TestSelectEclipseCase:
    def test_name(self) -> None:
        assert SelectEclipseCase.name == "select_eclipse_case"

    def test_run_returns_input_case(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        loaded_grid_case: GridCase,
    ) -> None:
        task = SelectEclipseCase()
        input_data = SelectEclipseCaseInput(
            resinsight=rips_instance_model,
            case=loaded_grid_case,
        )
        result = task.run(input_data, ctx)

        assert result is loaded_grid_case
