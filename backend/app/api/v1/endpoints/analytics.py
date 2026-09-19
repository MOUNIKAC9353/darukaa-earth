from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_owned_site
from app.crud import crud_site_metric
from app.db.session import get_db
from app.models.site import Site
from app.schemas.site_metric import SiteMetricCreate, SiteMetricRead

router = APIRouter()


@router.post(
    "/sites/{site_id}/metrics", response_model=SiteMetricRead, status_code=status.HTTP_201_CREATED
)
def add_site_metric(
    metric_in: SiteMetricCreate,
    db: Session = Depends(get_db),
    site: Site = Depends(get_owned_site),
) -> SiteMetricRead:
    return crud_site_metric.create(db, metric_in=metric_in, site_id=site.id)


@router.get("/sites/{site_id}/metrics", response_model=list[SiteMetricRead])
def list_site_metrics(
    db: Session = Depends(get_db), site: Site = Depends(get_owned_site)
) -> list[SiteMetricRead]:
    return crud_site_metric.get_multi_by_site(db, site_id=site.id)
