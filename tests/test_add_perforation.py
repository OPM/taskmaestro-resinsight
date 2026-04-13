"""Tests for AddPerforation task."""

from __future__ import annotations

from unittest.mock import MagicMock

from taskekrabbe import ExecutionContext

from models import AddPerforationInput, PerforationOutput, RipsInstance, WellPath
from tasks.add_perforation import AddPerforation


class TestAddPerforation:
    def test_name(self) -> None:
        assert AddPerforation.name == "add_perforation"

    def test_run_adds_perforation(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
        well_path_model: WellPath,
        mock_well_path: MagicMock,
    ) -> None:
        mock_collection = MagicMock()
        mock_timeline = MagicMock()
        mock_collection.event_timeline.return_value = mock_timeline
        mock_rips_instance.project.descendants.return_value = [mock_collection]

        task = AddPerforation()
        input_data = AddPerforationInput(
            resinsight=rips_instance_model,
            well_path=well_path_model,
            event_date="2024-01-01",
            start_md=3000.0,
            end_md=3500.0,
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, PerforationOutput)
        assert result.value is mock_well_path
        assert result.start_md == 3000.0
        assert result.end_md == 3500.0
        mock_timeline.add_perf_event.assert_called_once_with(
            event_date="2024-01-01",
            well_path=mock_well_path,
            start_md=3000.0,
            end_md=3500.0,
            diameter=0.1,
            skin_factor=0.5,
            state="OPEN",
        )

    def test_run_with_different_parameters(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
        well_path_model: WellPath,
    ) -> None:
        mock_collection = MagicMock()
        mock_timeline = MagicMock()
        mock_collection.event_timeline.return_value = mock_timeline
        mock_rips_instance.project.descendants.return_value = [mock_collection]

        task = AddPerforation()
        input_data = AddPerforationInput(
            resinsight=rips_instance_model,
            well_path=well_path_model,
            event_date="2024-06-15",
            start_md=1000.0,
            end_md=1500.0,
        )
        result = task.run(input_data, ctx)

        assert result.start_md == 1000.0
        assert result.end_md == 1500.0
