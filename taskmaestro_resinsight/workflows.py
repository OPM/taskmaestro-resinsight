"""Workflows published through the ``taskmaestro.workflows`` entry-point group."""

from taskmaestro import Workflow

from .add_perforation import AddPerforation
from .connect_to_resinsight import ConnectToResInsight
from .export_completions import ExportCompletions
from .select_eclipse_case import SelectEclipseCase
from .select_well_path import SelectWellPath

# Entry points resolve objects rather than calling factories. Keeping the workflow
# as a module-level object also makes its input/output graph available to discovery
# clients without starting ResInsight.
resinsight_completions = (
    Workflow.builder("resinsight_completions")
    .add_task(ConnectToResInsight)
    .add_task(
        SelectEclipseCase,
        depends_on={"resinsight": ConnectToResInsight},
        config_fields=["case"],
    )
    .add_task(
        SelectWellPath,
        name="select_well_path_1",
        depends_on={"resinsight": ConnectToResInsight, "grid_case": SelectEclipseCase},
        config_fields=["well_path"],
    )
    .add_task(
        SelectWellPath,
        name="select_well_path_2",
        depends_on={"resinsight": ConnectToResInsight, "grid_case": SelectEclipseCase},
        config_fields=["well_path"],
    )
    .add_task(
        AddPerforation,
        name="add_perf_1",
        depends_on={
            "resinsight": ConnectToResInsight,
            "well_path": "select_well_path_1",
        },
        config_fields=["event_date", "start_md", "end_md"],
    )
    .add_task(
        AddPerforation,
        name="add_perf_2",
        depends_on={
            "resinsight": ConnectToResInsight,
            "well_path": "select_well_path_2",
        },
        config_fields=["event_date", "start_md", "end_md"],
    )
    .add_task(
        ExportCompletions,
        depends_on={
            "resinsight": ConnectToResInsight,
            "grid_case": SelectEclipseCase,
            "perforation_1": "add_perf_1",
            "perforation_2": "add_perf_2",
        },
        config_fields=["event_date", "export_path"],
    )
    .build()
)
