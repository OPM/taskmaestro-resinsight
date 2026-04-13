"""Tests for CreateGridView task."""

from __future__ import annotations

from unittest.mock import MagicMock

from taskekrabbe import ExecutionContext

from models import GridCase, GridView
from tasks.create_grid_view import CreateGridView


class TestCreateGridView:
    def test_name(self) -> None:
        assert CreateGridView.name == "create_grid_view"

    def test_run_creates_view(
        self,
        ctx: ExecutionContext,
        grid_case_model: GridCase,
        mock_eclipse_case: MagicMock,
    ) -> None:
        mock_view = MagicMock()
        mock_eclipse_case.create_view.return_value = mock_view

        task = CreateGridView()
        result = task.run(grid_case_model, ctx)

        assert isinstance(result, GridView)
        assert result.value is mock_view
        mock_eclipse_case.create_view.assert_called_once()
