from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.site import SiteRead


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_type: str = Field(default="carbon", pattern="^(carbon|biodiversity)$")


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    project_type: str
    owner_id: int
    created_at: datetime


class ProjectWithSites(ProjectRead):
    sites: list[SiteRead] = []
