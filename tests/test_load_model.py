"""Tests for LoadModel task."""

from __future__ import annotations

from unittest.mock import MagicMock

from taskekrabbe import ExecutionContext

from models import GridCase, LoadModelInput, RipsInstance
from tasks.load_model import LoadModel


class TestLoadModel:
    def test_name(self) -> None:
        assert LoadModel.name == "load_model"

    def test_run_loads_case(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
    ) -> None:
        mock_case = MagicMock()
        mock_case.name = "NORNE"
        mock_case.id = 1
        mock_rips_instance.project.load_case.return_value = mock_case

        task = LoadModel()
        input_data = LoadModelInput(resinsight=rips_instance_model, path="/path/to/NORNE.EGRID")
        result = task.run(input_data, ctx)

        assert isinstance(result, GridCase)
        assert result.value is mock_case
        mock_rips_instance.project.load_case.assert_called_once_with("/path/to/NORNE.EGRID")

    def test_run_propagates_error(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        mock_rips_instance: MagicMock,
    ) -> None:
        mock_rips_instance.project.load_case.side_effect = FileNotFoundError("File not found")

        task = LoadModel()
        input_data = LoadModelInput(resinsight=rips_instance_model, path="/bad/path.EGRID")

        import pytest

        with pytest.raises(FileNotFoundError, match="File not found"):
            task.run(input_data, ctx)
