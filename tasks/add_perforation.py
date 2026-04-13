"""Task: Add perforation events to a well path."""

from __future__ import annotations

import rips

from taskekrabbe import ExecutionContext, Task

from models import AddPerforationInput, PerforationOutput


class AddPerforation(Task[AddPerforationInput, PerforationOutput]):
    """Add perforation events to a well path."""

    name = "add_perforation"

    def run(self, input: AddPerforationInput, ctx: ExecutionContext) -> PerforationOutput:
        instance = input.resinsight.value
        well = input.well_path.value
        ctx.logger.info(
            "Adding perforation to '%s' at MD %.1f-%.1f on %s",
            well.name,
            input.start_md,
            input.end_md,
            input.event_date,
        )
        collection = instance.project.descendants(rips.WellPathCollection)[0]
        timeline = collection.event_timeline()
        timeline.add_perf_event(
            event_date=input.event_date,
            well_path=well,
            start_md=input.start_md,
            end_md=input.end_md,
            diameter=0.1,
            skin_factor=0.5,
            state="OPEN",
        )

        return PerforationOutput(
            value=well,
            start_md=input.start_md,
            end_md=input.end_md,
        )
