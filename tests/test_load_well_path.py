"""Tests for LoadWellPath task."""

from __future__ import annotations

from unittest.mock import MagicMock

from taskekrabbe import ExecutionContext

from models import GridCase, LoadWellPathInput, RipsInstance, WellPath
from tasks.load_well_path import LoadWellPath


class TestLoadWellPath:
    def test_name(self) -> None:
        assert LoadWellPath.name == "load_well_path"

    def test_run_imports_well_path(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
        grid_case_model: GridCase,
    ) -> None:
        mock_wp = MagicMock()
        mock_wp.name = "B-2H"
        mock_collection = MagicMock()
        mock_collection.import_well_path.return_value = mock_wp
        mock_rips_instance.project.well_path_collection.return_value = mock_collection

        task = LoadWellPath()
        input_data = LoadWellPathInput(
            resinsight=rips_instance_model,
            grid_case=grid_case_model,
            path="/path/to/B-2H.json",
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, WellPath)
        assert result.value is mock_wp
        mock_collection.import_well_path.assert_called_once_with(file_name="/path/to/B-2H.json")

    def test_run_propagates_error(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
        grid_case_model: GridCase,
    ) -> None:
        mock_collection = MagicMock()
        mock_collection.import_well_path.side_effect = RuntimeError("Import failed")
        mock_rips_instance.project.well_path_collection.return_value = mock_collection

        task = LoadWellPath()
        input_data = LoadWellPathInput(
            resinsight=rips_instance_model,
            grid_case=grid_case_model,
            path="/bad/path.json",
        )

        import pytest

        with pytest.raises(RuntimeError, match="Import failed"):
            task.run(input_data, ctx)
