from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteMetricCreate(BaseModel):
    recorded_date: date
    carbon_tons: float = Field(ge=0)
    biodiversity_index: float = Field(ge=0, le=100)
    ndvi: float = Field(ge=-1, le=1)


class SiteMetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    recorded_date: date
    carbon_tons: float
    biodiversity_index: float
    ndvi: float
    created_at: datetime
