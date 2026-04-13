"""Tests for ConnectToResInsight task."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from taskekrabbe import ExecutionContext

from models import RipsInstance
from tasks.connect_to_resinsight import ConnectToResInsight


class TestConnectToResInsight:
    def test_name(self) -> None:
        assert ConnectToResInsight.name == "connect_to_resinsight"

    @patch("tasks.connect_to_resinsight.rips")
    def test_run_returns_rips_instance(self, mock_rips: MagicMock, ctx: ExecutionContext) -> None:
        mock_instance = MagicMock()
        mock_instance.location = "localhost:50051"
        mock_rips.Instance.find.return_value = mock_instance

        task = ConnectToResInsight()
        from taskekrabbe import EmptyConfig

        result = task.run(EmptyConfig(), ctx)

        assert isinstance(result, RipsInstance)
        assert result.value is mock_instance
        mock_rips.Instance.find.assert_called_once()

    @patch("tasks.connect_to_resinsight.rips")
    def test_run_raises_on_connection_failure(self, mock_rips: MagicMock, ctx: ExecutionContext) -> None:
        mock_rips.Instance.find.side_effect = ConnectionError("No ResInsight found")

        task = ConnectToResInsight()
        from taskekrabbe import EmptyConfig

        import pytest

        with pytest.raises(ConnectionError, match="No ResInsight found"):
            task.run(EmptyConfig(), ctx)
