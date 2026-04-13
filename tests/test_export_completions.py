"""Tests for ExportCompletions task."""

from __future__ import annotations

from unittest.mock import MagicMock

from taskekrabbe import ExecutionContext

from models import GridCase, PerforationOutput, RipsInstance
from tasks.export_completions import ExportCompletions


class TestExportCompletions:
    def test_name(self) -> None:
        assert ExportCompletions.name == "export_completions"

    def test_run_exports_completions(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
        grid_case_model: GridCase,
        mock_eclipse_case: MagicMock,
    ) -> None:
        mock_wp1 = MagicMock()
        mock_wp1.name = "B-2H"
        mock_wp2 = MagicMock()
        mock_wp2.name = "C-4H"

        perf1 = PerforationOutput(value=mock_wp1, start_md=3000.0, end_md=3500.0)
        perf2 = PerforationOutput(value=mock_wp2, start_md=2400.0, end_md=2600.0)

        mock_collection = MagicMock()
        mock_timeline = MagicMock()
        mock_collection.event_timeline.return_value = mock_timeline
        mock_rips_instance.project.descendants.return_value = [mock_collection]

        task = ExportCompletions()
        input_data = ExportCompletions.Inputs(
            resinsight=rips_instance_model,
            grid_case=grid_case_model,
            perforation_1=perf1,
            perforation_2=perf2,
            event_date="2024-05-01",
            export_path="/tmp/completions.txt",
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, ExportCompletions.Outputs)
        assert result.export_file == "/tmp/completions.txt"
        assert result.well_path_names == ["B-2H", "C-4H"]
        mock_timeline.set_timestamp.assert_called_once_with(timestamp="2024-05-01")
        mock_eclipse_case.export_well_path_completions.assert_called_once_with(
            time_step=0,
            well_path_names=["B-2H", "C-4H"],
            file_split="UNIFIED_FILE",
            include_perforations=True,
            custom_file_name="/tmp/completions.txt",
        )

    def test_inputs_model_fields(self) -> None:
        fields = ExportCompletions.Inputs.model_fields
        assert "resinsight" in fields
        assert "grid_case" in fields
        assert "perforation_1" in fields
        assert "perforation_2" in fields
        assert "event_date" in fields
        assert "export_path" in fields

    def test_outputs_model_fields(self) -> None:
        fields = ExportCompletions.Outputs.model_fields
        assert "export_file" in fields
        assert "well_path_names" in fields
