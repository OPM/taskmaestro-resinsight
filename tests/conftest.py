"""Shared fixtures for ResInsight task tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from taskekrabbe import ExecutionContext

from models import GridCase, PerforationOutput, RipsInstance, WellPath


@pytest.fixture
def ctx() -> ExecutionContext:
    return ExecutionContext()


@pytest.fixture
def mock_rips_instance() -> MagicMock:
    """Create a mock rips.Instance with common attributes."""
    instance = MagicMock()
    instance.location = "localhost:50051"
    return instance


@pytest.fixture
def rips_instance_model(mock_rips_instance: MagicMock) -> RipsInstance:
    """Wrapped RipsInstance model."""
    return RipsInstance(value=mock_rips_instance)


@pytest.fixture
def mock_eclipse_case() -> MagicMock:
    """Create a mock rips.EclipseCase."""
    case = MagicMock()
    case.name = "NORNE"
    case.id = 1
    return case


@pytest.fixture
def grid_case_model(mock_eclipse_case: MagicMock) -> GridCase:
    """Wrapped GridCase model."""
    return GridCase(value=mock_eclipse_case)


@pytest.fixture
def mock_well_path() -> MagicMock:
    """Create a mock rips.WellPath."""
    wp = MagicMock()
    wp.name = "B-2H"
    return wp


@pytest.fixture
def well_path_model(mock_well_path: MagicMock) -> WellPath:
    """Wrapped WellPath model."""
    return WellPath(value=mock_well_path)


@pytest.fixture
def perforation_output(mock_well_path: MagicMock) -> PerforationOutput:
    """A PerforationOutput fixture."""
    return PerforationOutput(value=mock_well_path, start_md=3000.0, end_md=3500.0)
