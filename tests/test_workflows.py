"""Tests for workflows exposed through package entry points."""

from taskmaestro import Workflow

from taskmaestro_resinsight.workflows import resinsight_completions


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
