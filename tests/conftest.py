"""Shared fixtures for ResInsight task tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import rips

from taskmaestro import ExecutionContext

from models import GridCase, RipsInstance, WellPath

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTMODELS_DIR = REPO_ROOT / "vendor" / "ResInsight" / "TestModels"
TEST10K_DIR = TESTMODELS_DIR / "TEST10K_FLT_LGR_NNC"

RESINSIGHT_EXECUTABLE = os.environ.get(
    "RESINSIGHT_EXECUTABLE",
    str(REPO_ROOT / "vendor" / "ResInsight" / "build" / "ResInsight"),
)


@pytest.fixture(scope="session")
def resinsight_instance() -> rips.Instance:
    """Launch a single ResInsight instance for the entire test session."""
    instance = rips.Instance.launch(
        resinsight_executable=RESINSIGHT_EXECUTABLE,
        console=True,
    )
    yield instance
    instance.exit()


@pytest.fixture
def ctx() -> ExecutionContext:
    return ExecutionContext()


@pytest.fixture
def rips_instance_model(resinsight_instance: rips.Instance) -> RipsInstance:
    """RipsInstance model wrapping the session instance."""
    return RipsInstance(value=resinsight_instance)


@pytest.fixture
def egrid_path() -> str:
    """Path to TEST10K_FLT_LGR_NNC.EGRID test model."""
    path = TEST10K_DIR / "TEST10K_FLT_LGR_NNC.EGRID"
    assert path.exists(), f"Test data not found: {path}"
    return str(path)


@pytest.fixture
def well_path_a() -> str:
    """Path to wellpath_a.dev test file."""
    path = TEST10K_DIR / "wellpath_a.dev"
    assert path.exists(), f"Test data not found: {path}"
    return str(path)


@pytest.fixture
def well_path_b() -> str:
    """Path to wellpath_b.dev test file."""
    path = TEST10K_DIR / "wellpath_b.dev"
    assert path.exists(), f"Test data not found: {path}"
    return str(path)


@pytest.fixture
def loaded_grid_case(
    resinsight_instance: rips.Instance,
    egrid_path: str,
) -> GridCase:
    """Load the test EGRID and return a GridCase model."""
    case = resinsight_instance.project.load_case(egrid_path)
    return GridCase(value=case)


@pytest.fixture
def loaded_well_path(
    resinsight_instance: rips.Instance,
    loaded_grid_case: GridCase,
    well_path_a: str,
) -> WellPath:
    """Import wellpath_a.dev and return a WellPath model."""
    collection = resinsight_instance.project.well_path_collection()
    wp = collection.import_well_path(file_name=well_path_a)
    return WellPath(value=wp)
