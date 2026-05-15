"""Tests for LoadModel task."""

from __future__ import annotations

import pytest

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.models import GridCase, LoadModelInput, RipsInstance
from taskmaestro_resinsight.load_model import LoadModel


class TestLoadModel:
    def test_name(self) -> None:
        assert LoadModel.name == "load_model"

    def test_run_loads_case(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        egrid_path: str,
    ) -> None:
        task = LoadModel()
        input_data = LoadModelInput(resinsight=rips_instance_model, path=egrid_path)
        result = task.run(input_data, ctx)

        assert isinstance(result, GridCase)
        assert result.value.id > 0

    def test_run_nonexistent_file_raises(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
    ) -> None:
        task = LoadModel()
        input_data = LoadModelInput(
            resinsight=rips_instance_model,
            path="/nonexistent/file.EGRID",
        )
        with pytest.raises(Exception):
            task.run(input_data, ctx)
