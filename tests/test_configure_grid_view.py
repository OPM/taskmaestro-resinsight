"""Tests for ConfigureGridView task."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
import rips
from pydantic import ValidationError
from taskmaestro import ExecutionContext

from taskmaestro_resinsight.configure_grid_view import ConfigureGridView
from taskmaestro_resinsight.models import ConfigureGridViewInput, GridView


class TestConfigureGridView:
    def test_name(self) -> None:
        assert ConfigureGridView.name == "configure_grid_view"

    def test_run_applies_result_and_time_step(self, ctx: ExecutionContext) -> None:
        view = Mock(spec=rips.View)
        grid_view = GridView(value=view)
        input_data = ConfigureGridViewInput(
            grid_view=grid_view,
            result_type="DYNAMIC_NATIVE",
            result_variable="PRESSURE",
            time_step=4,
        )

        result = ConfigureGridView().run(input_data, ctx)

        assert result is grid_view
        view.apply_cell_result.assert_called_once_with(
            result_type="DYNAMIC_NATIVE",
            result_variable="PRESSURE",
        )
        view.set_time_step.assert_called_once_with(time_step=4)

    @pytest.mark.parametrize("time_step", [-1, -10])
    def test_rejects_negative_time_step(self, time_step: int) -> None:
        with pytest.raises(ValidationError):
            ConfigureGridViewInput(
                grid_view=GridView(value=Mock(spec=rips.View)),
                result_type="STATIC_NATIVE",
                result_variable="PORO",
                time_step=time_step,
            )

    def test_rejects_unknown_result_type(self) -> None:
        with pytest.raises(ValidationError):
            ConfigureGridViewInput(
                grid_view=GridView(value=Mock(spec=rips.View)),
                result_type="UNKNOWN",  # type: ignore[arg-type]
                result_variable="PORO",
            )
