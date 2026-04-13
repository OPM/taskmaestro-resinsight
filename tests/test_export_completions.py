"""Tests for ExportCompletions task — full pipeline integration test."""

from __future__ import annotations

from taskekrabbe import ExecutionContext

from models import (
    AddPerforationInput,
    LoadModelInput,
    LoadWellPathInput,
    RipsInstance,
)
from tasks.add_perforation import AddPerforation
from tasks.export_completions import ExportCompletions
from tasks.load_model import LoadModel
from tasks.load_well_path import LoadWellPath


class TestExportCompletions:
    def test_name(self) -> None:
        assert ExportCompletions.name == "export_completions"

    def test_full_pipeline(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        egrid_path: str,
        well_path_a: str,
        well_path_b: str,
        tmp_path: object,
    ) -> None:
        # Load model
        grid_case = LoadModel().run(
            LoadModelInput(resinsight=rips_instance_model, path=egrid_path),
            ctx,
        )

        # Load two well paths
        wp1 = LoadWellPath().run(
            LoadWellPathInput(
                resinsight=rips_instance_model,
                grid_case=grid_case,
                path=well_path_a,
            ),
            ctx,
        )
        wp2 = LoadWellPath().run(
            LoadWellPathInput(
                resinsight=rips_instance_model,
                grid_case=grid_case,
                path=well_path_b,
            ),
            ctx,
        )

        # Add perforations
        perf1 = AddPerforation().run(
            AddPerforationInput(
                resinsight=rips_instance_model,
                well_path=wp1,
                event_date="2024-01-01",
                start_md=3000.0,
                end_md=3500.0,
            ),
            ctx,
        )
        perf2 = AddPerforation().run(
            AddPerforationInput(
                resinsight=rips_instance_model,
                well_path=wp2,
                event_date="2024-02-01",
                start_md=2400.0,
                end_md=2600.0,
            ),
            ctx,
        )

        # Export completions
        export_path = str(tmp_path / "completions.txt")  # type: ignore[operator]
        task = ExportCompletions()
        result = task.run(
            ExportCompletions.Inputs(
                resinsight=rips_instance_model,
                grid_case=grid_case,
                perforation_1=perf1,
                perforation_2=perf2,
                event_date="2024-05-01",
                export_path=export_path,
            ),
            ctx,
        )

        assert isinstance(result, ExportCompletions.Outputs)
        assert result.export_file == export_path
        assert len(result.well_path_names) == 2

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
