from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.site_metric import SiteMetric


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    area_hectares: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Polygon boundary of the site, stored as WGS84 (SRID 4326) geometry via PostGIS.
    geom: Mapped[str] = mapped_column(Geometry(geometry_type="POLYGON", srid=4326), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped["Project"] = relationship(back_populates="sites")
    metrics: Mapped[list["SiteMetric"]] = relationship(
        back_populates="site", cascade="all, delete-orphan", order_by="SiteMetric.recorded_date"
    )
