"""Tests for ConnectToResInsight task."""

from __future__ import annotations

import os

import rips

from taskmaestro import EmptyConfig, ExecutionContext

from models import RipsInstance
from tasks.connect_to_resinsight import ConnectToResInsight


class TestConnectToResInsight:
    def test_name(self) -> None:
        assert ConnectToResInsight.name == "connect_to_resinsight"

    def test_run_connects(
        self,
        resinsight_instance: rips.Instance,
        ctx: ExecutionContext,
    ) -> None:
        """Verify ConnectToResInsight finds the session instance.

        The session fixture launches on a random port, so we set
        RESINSIGHT_GRPC_PORT so that rips.Instance.find() scans the right range.
        """
        port = int(resinsight_instance.location.split(":")[-1])
        old_env = os.environ.get("RESINSIGHT_GRPC_PORT")
        os.environ["RESINSIGHT_GRPC_PORT"] = str(port)
        try:
            task = ConnectToResInsight()
            result = task.run(EmptyConfig(), ctx)

            assert isinstance(result, RipsInstance)
            assert result.value is not None
        finally:
            if old_env is None:
                os.environ.pop("RESINSIGHT_GRPC_PORT", None)
            else:
                os.environ["RESINSIGHT_GRPC_PORT"] = old_env
