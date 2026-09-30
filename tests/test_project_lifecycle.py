"""Tests for project and application lifecycle tasks."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
import rips
from pydantic import ValidationError
from taskmaestro import ExecutionContext

from taskmaestro_resinsight.close_project import CloseProject
from taskmaestro_resinsight.exit_resinsight import ExitResInsight
from taskmaestro_resinsight.models import (
    ExitResult,
    OpenProjectInput,
    RipsInstance,
    SaveProjectInput,
)
from taskmaestro_resinsight.open_project import OpenProject
from taskmaestro_resinsight.save_project import SaveProject


@pytest.fixture
def mocked_instance() -> tuple[RipsInstance, Mock, Mock]:
    instance = Mock(spec=rips.Instance)
    project = Mock(spec=rips.Project)
    instance.project = project
    return RipsInstance(value=instance), instance, project


class TestOpenProject:
    def test_name(self) -> None:
        assert OpenProject.name == "open_project"

    def test_run_opens_project_and_returns_instance(
        self,
        ctx: ExecutionContext,
        mocked_instance: tuple[RipsInstance, Mock, Mock],
    ) -> None:
        model, _, project = mocked_instance

        result = OpenProject().run(
            OpenProjectInput(resinsight=model, path="model.rsp"), ctx
        )

        assert result is model
        project.open.assert_called_once_with("model.rsp")

    def test_rejects_empty_path(
        self, mocked_instance: tuple[RipsInstance, Mock, Mock]
    ) -> None:
        model, _, _ = mocked_instance
        with pytest.raises(ValidationError):
            OpenProjectInput(resinsight=model, path="")


class TestSaveProject:
    def test_name(self) -> None:
        assert SaveProject.name == "save_project"

    @pytest.mark.parametrize("path", ["saved.rsp", ""])
    def test_run_saves_project_and_returns_instance(
        self,
        path: str,
        ctx: ExecutionContext,
        mocked_instance: tuple[RipsInstance, Mock, Mock],
    ) -> None:
        model, _, project = mocked_instance

        result = SaveProject().run(SaveProjectInput(resinsight=model, path=path), ctx)

        assert result is model
        project.save.assert_called_once_with(path)


class TestCloseProject:
    def test_name(self) -> None:
        assert CloseProject.name == "close_project"

    def test_run_closes_project_and_returns_instance(
        self,
        ctx: ExecutionContext,
        mocked_instance: tuple[RipsInstance, Mock, Mock],
    ) -> None:
        model, _, project = mocked_instance

        result = CloseProject().run(model, ctx)

        assert result is model
        project.close.assert_called_once_with()


class TestExitResInsight:
    def test_name(self) -> None:
        assert ExitResInsight.name == "exit_resinsight"

    def test_run_exits_and_returns_confirmation(
        self,
        ctx: ExecutionContext,
        mocked_instance: tuple[RipsInstance, Mock, Mock],
    ) -> None:
        model, instance, _ = mocked_instance

        result = ExitResInsight().run(model, ctx)

        assert result == ExitResult(exited=True)
        instance.exit.assert_called_once_with()
