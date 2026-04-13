"""Tests for LaunchResInsight task."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from taskekrabbe import ExecutionContext

from models import RipsInstance
from tasks.launch_resinsight import LaunchResInsight, LaunchResInsightInput


class TestLaunchResInsight:
    def test_name(self) -> None:
        assert LaunchResInsight.name == "launch_resinsight"

    @patch("tasks.launch_resinsight.rips")
    def test_run_launches_instance(self, mock_rips: MagicMock, ctx: ExecutionContext) -> None:
        mock_instance = MagicMock()
        mock_instance.location = "localhost:50051"
        mock_rips.Instance.launch.return_value = mock_instance

        task = LaunchResInsight()
        input_data = LaunchResInsightInput(resinsight_executable="/usr/bin/ResInsight", console=True)
        result = task.run(input_data, ctx)

        assert isinstance(result, RipsInstance)
        assert result.value is mock_instance
        mock_rips.Instance.launch.assert_called_once_with(
            resinsight_executable="/usr/bin/ResInsight",
            console=True,
        )

    @patch("tasks.launch_resinsight.rips")
    def test_run_with_defaults(self, mock_rips: MagicMock, ctx: ExecutionContext) -> None:
        mock_instance = MagicMock()
        mock_instance.location = "localhost:50051"
        mock_rips.Instance.launch.return_value = mock_instance

        task = LaunchResInsight()
        input_data = LaunchResInsightInput()
        result = task.run(input_data, ctx)

        assert isinstance(result, RipsInstance)
        mock_rips.Instance.launch.assert_called_once_with(
            resinsight_executable="",
            console=True,
        )
