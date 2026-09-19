from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.site import Site


class SiteMetric(Base):
    """A single time-series observation of a site's ecological performance."""

    __tablename__ = "site_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"))
    recorded_date: Mapped[date] = mapped_column(Date, nullable=False)
    carbon_tons: Mapped[float] = mapped_column(Float, nullable=False)
    biodiversity_index: Mapped[float] = mapped_column(Float, nullable=False)
    ndvi: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    site: Mapped["Site"] = relationship(back_populates="metrics")
