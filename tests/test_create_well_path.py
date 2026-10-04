"""Tests for CreateWellPath task (creates a modeled well path)."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.create_well_path import CreateWellPath
from taskmaestro_resinsight.models import (
    CreateWellPathInput,
    RipsInstance,
    Vec3,
    WellPath,
)


class TestCreateWellPath:
    def test_name(self) -> None:
        assert CreateWellPath.name == "create_well_path"

    def test_run_creates_modeled_well_path(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
    ) -> None:
        task = CreateWellPath()
        input_data = CreateWellPathInput(
            resinsight=rips_instance_model,
            name="Test Well-1",
            reference_point=Vec3(x=457196, y=7322270, z=2742),
            targets=[
                Vec3(x=0, y=0, z=0),
                Vec3(x=454.28, y=250, z=-10),
                Vec3(x=1054.28, y=250, z=-50),
            ],
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, WellPath)
        assert result.value.name == "Test Well-1"
        geometry = result.value.well_path_geometry()
        assert geometry.reference_point == [457196, 7322270, 2742]
        assert len(geometry.well_path_targets()) == 3
