"""Tests for workflows exposed through package entry points."""

from taskmaestro import (
    Workflow,
    get_registered_task,
    get_registered_workflow,
    registered_task_names,
    registered_workflow_names,
)

from taskmaestro_resinsight.add_perforation import AddPerforation
from taskmaestro_resinsight.connect_to_resinsight import ConnectToResInsight
from taskmaestro_resinsight.create_grid_view import CreateGridView
from taskmaestro_resinsight.export_completions import ExportCompletions
from taskmaestro_resinsight.import_grid_property import ImportGridProperty
from taskmaestro_resinsight.launch_resinsight import LaunchResInsight
from taskmaestro_resinsight.load_model import LoadModel
from taskmaestro_resinsight.load_well_path import LoadWellPath
from taskmaestro_resinsight.select_eclipse_case import SelectEclipseCase
from taskmaestro_resinsight.select_well_path import SelectWellPath
from taskmaestro_resinsight.workflows import resinsight_completions

EXPECTED_TASKS = {
    "resinsight.add_perforation": AddPerforation,
    "resinsight.connect": ConnectToResInsight,
    "resinsight.create_grid_view": CreateGridView,
    "resinsight.export_completions": ExportCompletions,
    "resinsight.launch": LaunchResInsight,
    "resinsight.import_grid_property": ImportGridProperty,
    "resinsight.load_model": LoadModel,
    "resinsight.load_well_path": LoadWellPath,
    "resinsight.select_eclipse_case": SelectEclipseCase,
    "resinsight.select_well_path": SelectWellPath,
}


def test_task_entry_points_are_discoverable() -> None:
    assert EXPECTED_TASKS.keys() <= registered_task_names()
    for name, task in EXPECTED_TASKS.items():
        assert get_registered_task(name) is task


def test_workflow_entry_point_is_discoverable() -> None:
    assert "resinsight.completions" in registered_workflow_names()
    assert get_registered_workflow("resinsight.completions") is resinsight_completions


def test_registered_completions_workflow() -> None:
    assert isinstance(resinsight_completions, Workflow)
    assert resinsight_completions.name == "resinsight_completions"
    assert resinsight_completions.result_task_name == "export_completions"
    assert [name for name, _ in resinsight_completions.topological_order()] == [
        "connect_to_resinsight",
        "select_eclipse_case",
        "select_well_path_1",
        "add_perf_1",
        "select_well_path_2",
        "add_perf_2",
        "export_completions",
    ]
