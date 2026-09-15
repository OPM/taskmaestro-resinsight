"""Tests for LoadRegularSurface."""

from __future__ import annotations

from taskmaestro import ExecutionContext

from taskmaestro_resinsight.load_regular_surface import LoadRegularSurface
from taskmaestro_resinsight.models import (
    LoadRegularSurfaceInput,
    RegularSurface,
    RipsInstance,
)


class TestLoadRegularSurface:
    def test_name(self) -> None:
        assert LoadRegularSurface.name == "load_regular_surface"

    def test_run_imports_regular_surface(
        self,
        ctx: ExecutionContext,
        rips_instance_model: RipsInstance,
        regular_surface_path: str,
    ) -> None:
        result = LoadRegularSurface().run(
            LoadRegularSurfaceInput(
                resinsight=rips_instance_model,
                path=regular_surface_path,
            ),
            ctx,
        )

        assert isinstance(result, RegularSurface)
        assert result.value is not None
