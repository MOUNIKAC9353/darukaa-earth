from sqlalchemy.orm import Session, joinedload

from app.models.project import Project
from app.models.site import Site
from app.schemas.site import SiteCreate
from app.utils.geo import geojson_to_wkb, polygon_area_hectares


def create(db: Session, site_in: SiteCreate, project_id: int) -> Site:
    site = Site(
        name=site_in.name,
        project_id=project_id,
        geom=geojson_to_wkb(site_in.geometry),
        area_hectares=polygon_area_hectares(site_in.geometry),
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def get(db: Session, site_id: int) -> Site | None:
    return db.query(Site).filter(Site.id == site_id).first()


def get_multi_by_project(db: Session, project_id: int) -> list[Site]:
    return db.query(Site).filter(Site.project_id == project_id).order_by(Site.created_at).all()


def get_multi_by_owner(db: Session, owner_id: int) -> list[Site]:
    """All sites across every project owned by the given user, for cross-project map views."""
    return (
        db.query(Site)
        .join(Project, Site.project_id == Project.id)
        .filter(Project.owner_id == owner_id)
        .options(joinedload(Site.project))
        .order_by(Site.created_at)
        .all()
    )
