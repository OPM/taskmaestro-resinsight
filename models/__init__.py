"""Pydantic models for ResInsight tasks."""

from __future__ import annotations

import rips
from pydantic import BaseModel, ConfigDict

from taskekrabbe import ObjectModel


class RipsInstance(ObjectModel[rips.Instance]):
    """Active connection to a running ResInsight application."""


class FilePath(BaseModel):
    """A file path provided via config."""

    path: str


class GridCase(ObjectModel[rips.EclipseCase]):
    """Loaded Eclipse reservoir grid case."""


class GridView(ObjectModel[rips.View]):
    """Grid view on a loaded Eclipse case."""


class WellPath(ObjectModel[rips.WellPath]):
    """Imported well trajectory."""


class LoadModelInput(BaseModel):
    """Input for LoadModel: RipsInstance from upstream, file path from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    path: str


class LoadWellPathInput(BaseModel):
    """Input for LoadWellPath: RipsInstance from upstream, file path from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    grid_case: GridCase
    path: str


class AddPerforationInput(BaseModel):
    """Input for AddPerforation: RipsInstance + well from upstream, MD range from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    well_path: WellPath
    event_date: str
    start_md: float
    end_md: float


class PerforationOutput(ObjectModel[rips.WellPath]):
    """Output of AddPerforation: perforation interval details."""

    start_md: float
    end_md: float
