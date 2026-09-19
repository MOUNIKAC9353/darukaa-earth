from sqlalchemy.orm import Session

from app.models.site_metric import SiteMetric
from app.schemas.site_metric import SiteMetricCreate


def create(db: Session, metric_in: SiteMetricCreate, site_id: int) -> SiteMetric:
    metric = SiteMetric(site_id=site_id, **metric_in.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def get_multi_by_site(db: Session, site_id: int) -> list[SiteMetric]:
    return (
        db.query(SiteMetric)
        .filter(SiteMetric.site_id == site_id)
        .order_by(SiteMetric.recorded_date)
        .all()
    )
