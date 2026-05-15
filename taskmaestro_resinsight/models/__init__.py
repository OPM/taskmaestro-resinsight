"""Pydantic models for ResInsight tasks."""

from __future__ import annotations

import rips
import datetime
from pydantic import BaseModel, ConfigDict, Field

from taskmaestro import ObjectModel


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
    """Input for LoadModel: RipsInstance from upstream, case selected via config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    case: GridCase = Field(description="Case to use")


class LoadWellPathInput(BaseModel):
    """Input for LoadWellPath: RipsInstance from upstream, well path selected via config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    grid_case: GridCase
    well_path: WellPath = Field(description="Well path to use")


class AddPerforationInput(BaseModel):
    """Input for AddPerforation: RipsInstance + well from upstream, MD range from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    well_path: WellPath
    event_date: datetime.date = Field(description="Perforation event date")
    start_md: float
    end_md: float


class PerforationOutput(ObjectModel[rips.WellPath]):
    """Output of AddPerforation: perforation interval details."""

    start_md: float
    end_md: float
