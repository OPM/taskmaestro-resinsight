"""Task: Import a regular surface from disk."""

from __future__ import annotations

from taskmaestro import ExecutionContext, Task

from .models import LoadRegularSurfaceInput, RegularSurface


class LoadRegularSurface(Task[LoadRegularSurfaceInput, RegularSurface]):
    """Import a regular surface file and wrap it as a RegularSurface."""

    name = "load_regular_surface"

    def run(
        self, input: LoadRegularSurfaceInput, ctx: ExecutionContext
    ) -> RegularSurface:
        ctx.logger.info("Loading regular surface from '%s'", input.path)
        surface = input.resinsight.value.project.surface_folder().import_surface(
            file_name=input.path
        )
        ctx.logger.info("Loaded regular surface")
        return RegularSurface(value=surface)
