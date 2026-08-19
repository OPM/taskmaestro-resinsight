"""Tests for AddPerforation task."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.add_perforation import AddPerforation
from taskmaestro_resinsight.models import (
    AddPerforationInput,
    PerforationOutput,
    RipsInstance,
    WellPath,
)


class TestAddPerforation:
    def test_name(self) -> None:
        assert AddPerforation.name == "add_perforation"

    def test_run_adds_perforation(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        loaded_well_path: WellPath,
    ) -> None:
        task = AddPerforation()
        input_data = AddPerforationInput(
            resinsight=rips_instance_model,
            well_path=loaded_well_path,
            event_date="2024-01-01",
            start_md=3000.0,
            end_md=3500.0,
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, PerforationOutput)
        assert result.start_md == 3000.0
        assert result.end_md == 3500.0
