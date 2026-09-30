"""Pydantic models for ResInsight tasks."""

from __future__ import annotations

import datetime
from typing import Literal

import rips
from pydantic import BaseModel, ConfigDict, Field
from taskmaestro import ObjectModel


class RipsInstance(ObjectModel[rips.Instance]):
    """Active connection to a running ResInsight application."""


class FilePath(BaseModel):
    """A file path provided via config."""

    path: str


class GridCase(ObjectModel[rips.Reservoir]):
    """Loaded Eclipse reservoir grid case."""


class RegularSurface(ObjectModel[rips.Surface]):
    """Loaded regular surface file."""


class GridView(ObjectModel[rips.View]):
    """Grid view on a loaded Eclipse case."""


class ConfigureGridViewInput(BaseModel):
    """Cell result and time step to display in a grid view."""

    grid_view: GridView
    result_type: Literal[
        "DYNAMIC_NATIVE",
        "STATIC_NATIVE",
        "SOURSIMRL",
        "GENERATED",
        "INPUT_PROPERTY",
        "FORMATION_NAMES",
        "ALLAN_DIAGRAMS",
        "FLOW_DIAGNOSTICS",
        "INJECTION_FLOODING",
    ]
    result_variable: str = Field(min_length=1)
    time_step: int = Field(default=0, ge=0)


class WellPath(ObjectModel[rips.WellPath]):
    """Imported well trajectory."""


class SelectEclipseCaseInput(BaseModel):
    """Input for SelectEclipseCase: RipsInstance from upstream, case selected via config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    case: GridCase = Field(description="Case to use")


class SelectWellPathInput(BaseModel):
    """Input for SelectWellPath: RipsInstance from upstream, well path selected via config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    grid_case: GridCase
    well_path: WellPath = Field(description="Well path to use")


class LoadModelInput(BaseModel):
    """Input for LoadModel: RipsInstance from upstream, path from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    path: str = Field(description="Path to the .EGRID file to load")


class OpenProjectInput(BaseModel):
    """Input for opening a ResInsight project file."""

    resinsight: RipsInstance
    path: str = Field(min_length=1, description="Path to the .rsp project file")


class SaveProjectInput(BaseModel):
    """Input for saving the current ResInsight project."""

    resinsight: RipsInstance
    path: str = Field(
        default="",
        description="Destination .rsp path; empty saves to the current project file",
    )


class ExitResult(BaseModel):
    """Confirmation that the ResInsight exit command was sent."""

    exited: bool


class LoadWellPathInput(BaseModel):
    """Input for LoadWellPath: RipsInstance + grid_case from upstream, path from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    grid_case: GridCase
    path: str = Field(description="Path to the .dev well-trajectory file to load")


class LoadRegularSurfaceInput(BaseModel):
    """Input for LoadRegularSurface: RipsInstance + path from config."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    path: str = Field(description="Path to the regular surface file to load")


class ImportGridPropertyInput(BaseModel):
    """Input for ImportGridProperty: RipsInstance, case, and property paths."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    resinsight: RipsInstance
    grid_case: GridCase
    paths: list[str] = Field(description="Paths to grid property files to load")


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
