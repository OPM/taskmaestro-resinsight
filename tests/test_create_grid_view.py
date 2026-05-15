"""Tests for CreateGridView task."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from models import GridCase, GridView
from tasks.create_grid_view import CreateGridView


class TestCreateGridView:
    def test_name(self) -> None:
        assert CreateGridView.name == "create_grid_view"

    def test_run_creates_view(
        self,
        ctx: ExecutionContext,
        loaded_grid_case: GridCase,
    ) -> None:
        task = CreateGridView()
        result = task.run(loaded_grid_case, ctx)

        assert isinstance(result, GridView)
        assert result.value is not None
