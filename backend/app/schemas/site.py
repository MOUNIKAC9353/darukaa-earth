from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GeoJSONPolygon(BaseModel):
    """A GeoJSON Polygon geometry, e.g. drawn by the Mapbox GL Draw control."""

    type: Literal["Polygon"] = "Polygon"
    coordinates: list[list[tuple[float, float]]]


class SiteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    geometry: GeoJSONPolygon


class SiteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    area_hectares: float | None
    geometry: GeoJSONPolygon
    created_at: datetime


class SiteWithProject(SiteRead):
    """A site enriched with its parent project's name, for cross-project map views."""

    project_name: str
