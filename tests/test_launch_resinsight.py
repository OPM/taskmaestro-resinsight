"""Tests for LaunchResInsight task."""

from __future__ import annotations


from taskmaestro import ExecutionContext

from models import RipsInstance
from tests.conftest import RESINSIGHT_EXECUTABLE
from tasks.launch_resinsight import LaunchResInsight, LaunchResInsightInput


class TestLaunchResInsight:
    def test_name(self) -> None:
        assert LaunchResInsight.name == "launch_resinsight"

    def test_run_launches_instance(self, ctx: ExecutionContext) -> None:
        task = LaunchResInsight()
        input_data = LaunchResInsightInput(
            resinsight_executable=RESINSIGHT_EXECUTABLE,
            console=True,
        )
        result = task.run(input_data, ctx)

        assert isinstance(result, RipsInstance)
        assert result.value is not None
        result.value.exit()
