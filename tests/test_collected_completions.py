"""Validate the collection and mapped-well example without a live ResInsight."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from taskmaestro.dependencies import CollectionRef
from taskmaestro.yaml_config import _load_workflow_only

from taskmaestro_resinsight.add_full_length_perforation import (
    AddFullLengthPerforation,
    AddFullLengthPerforationInput,
    AddFullLengthPerforations,
    AddFullLengthPerforationsInput,
)
from taskmaestro_resinsight.add_perforation import AddPerforation
from taskmaestro_resinsight.export_completions import ExportCollectedCompletions
from taskmaestro_resinsight.merge_perforations import (
    MergePerforations,
    MergePerforationsInput,
)
from taskmaestro_resinsight.models import PerforationOutput, RipsInstance, WellPath

EXAMPLE = (
    Path(__file__).resolve().parents[1] / "workflows/resinsight_collected_completions"
)


def test_example_graph() -> None:
    workflow, config = _load_workflow_only(
        EXAMPLE / "workflow.yaml", EXAMPLE / "input.yaml"
    )
    assert workflow.result_task_name == "export_collected_completions"
    assert workflow.get_task_map("load_wells").over == "paths"
    assert config.get_config_for_task("load_wells")["paths"] == {
        "third": "/path/to/third.dev",
        "fourth": "/path/to/fourth.dev",
    }
    assert workflow.get_dependencies("add_full_length_perforations")["well_paths"] == (
        "load_wells",
        "root",
    )
    merged = workflow.get_dependencies("merge_perforations")
    assert isinstance(merged["selected"], CollectionRef)
    assert merged["selected"].kind == "positional"
    assert merged["loaded"] == ("add_full_length_perforations", "perforations")
    deps = workflow.get_dependencies("export_collected_completions")
    assert deps["perforations"] == ("merge_perforations", "perforations")


def test_collected_export_combines_well_names() -> None:
    task = ExportCollectedCompletions()
    task._export = Mock(
        return_value=ExportCollectedCompletions.Outputs(
            export_file="/tmp/test.txt", well_path_names=["A", "B", "C"]
        )
    )
    perf_a = PerforationOutput.model_construct(
        value=SimpleNamespace(name="A"), start_md=1, end_md=2
    )
    perf_b = PerforationOutput.model_construct(
        value=SimpleNamespace(name="B"), start_md=1, end_md=2
    )
    perf_c = PerforationOutput.model_construct(
        value=SimpleNamespace(name="C"), start_md=0, end_md=3
    )
    inputs = task.Inputs.model_construct(
        resinsight=Mock(),
        grid_case=Mock(),
        perforations=[perf_a, perf_b, perf_c],
        event_date="2024-05-01",
        export_path="/tmp/test.txt",
    )
    task.run(inputs, Mock())
    assert task._export.call_args.args[2] == ["A", "B", "C"]


def test_merge_flattens_selected_and_loaded_perforations() -> None:
    selected = PerforationOutput.model_construct(
        value=SimpleNamespace(name="A"), start_md=1, end_md=2
    )
    imported = PerforationOutput.model_construct(
        value=SimpleNamespace(name="B"), start_md=0, end_md=10
    )
    result = MergePerforations().run(
        MergePerforationsInput(selected=[selected], loaded={"well_b": imported}),
        Mock(),
    )
    assert result.perforations == [selected, imported]


def test_full_length_uses_trajectory_md_bounds() -> None:
    well = Mock(name="well")
    well.name = "A"
    well.trajectory_properties.return_value = {"measured_depth": [125.0, 140.0, 200.0]}
    wrapper = WellPath.model_construct(value=well)
    perf = PerforationOutput.model_construct(value=well, start_md=125.0, end_md=200.0)
    with patch.object(AddPerforation, "run", return_value=perf) as add:
        result = AddFullLengthPerforation().run(
            AddFullLengthPerforationInput.model_construct(
                resinsight=RipsInstance.model_construct(value=Mock()),
                well_path=wrapper,
                event_date="2024-01-01",
            ),
            Mock(),
        )
    assert result is perf
    assert add.call_args.args[0].start_md == 125.0
    assert add.call_args.args[0].end_md == 200.0


def test_full_length_rejects_empty_trajectory() -> None:
    import pytest

    well = Mock()
    well.name = "empty"
    well.trajectory_properties.return_value = {"measured_depth": []}
    with pytest.raises(ValueError, match="no valid MD range"):
        AddFullLengthPerforation().run(
            AddFullLengthPerforationInput.model_construct(
                resinsight=Mock(),
                well_path=WellPath.model_construct(value=well),
                event_date="2024-01-01",
            ),
            Mock(),
        )


def test_batch_preserves_mapping_keys() -> None:
    a = WellPath.model_construct(value=Mock())
    b = WellPath.model_construct(value=Mock())
    with patch.object(
        AddFullLengthPerforation,
        "run",
        side_effect=[
            PerforationOutput.model_construct(value=a.value, start_md=1, end_md=2),
            PerforationOutput.model_construct(value=b.value, start_md=3, end_md=4),
        ],
    ):
        result = AddFullLengthPerforations().run(
            AddFullLengthPerforationsInput.model_construct(
                resinsight=RipsInstance.model_construct(value=Mock()),
                well_paths={"a": a, "b": b},
                event_date="2024-01-01",
            ),
            Mock(),
        )
    assert list(result.perforations) == ["a", "b"]
