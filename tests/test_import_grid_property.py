"""Tests for ImportGridProperty."""

from __future__ import annotations

import rips
from taskmaestro import ExecutionContext

from taskmaestro_resinsight.import_grid_property import ImportGridProperty
from taskmaestro_resinsight.load_model import LoadModel
from taskmaestro_resinsight.models import (
    GridCase,
    ImportGridPropertyInput,
    LoadModelInput,
    RipsInstance,
)


class TestImportGridProperty:
    def test_name(self) -> None:
        assert ImportGridProperty.name == "import_grid_property"

    def test_run_imports_property(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        roff_grid_path: str,
        roff_property_path: str,
    ) -> None:
        grid_case = LoadModel().run(
            LoadModelInput(
                resinsight=rips_instance_model,
                path=roff_grid_path,
            ),
            ctx,
        )
        result = ImportGridProperty().run(
            ImportGridPropertyInput(
                resinsight=rips_instance_model,
                grid_case=grid_case,
                paths=[roff_property_path],
            ),
            ctx,
        )

        assert isinstance(result, GridCase)
        assert "PORO" in result.value.available_properties(
            rips.PropertyType.INPUT_PROPERTY
        )
