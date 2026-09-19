from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_project, get_owned_site
from app.crud import crud_site
from app.db.session import get_db
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.site import SiteCreate, SiteRead, SiteWithProject
from app.utils.geo import wkb_to_geojson

router = APIRouter()


def _site_to_read(site: Site) -> SiteRead:
    return SiteRead(
        id=site.id,
        project_id=site.project_id,
        name=site.name,
        area_hectares=site.area_hectares,
        geometry=wkb_to_geojson(site.geom),
        created_at=site.created_at,
    )


@router.post(
    "/projects/{project_id}/sites", response_model=SiteRead, status_code=status.HTTP_201_CREATED
)
def create_site(
    site_in: SiteCreate,
    db: Session = Depends(get_db),
    project: Project = Depends(get_owned_project),
) -> SiteRead:
    site = crud_site.create(db, site_in=site_in, project_id=project.id)
    return _site_to_read(site)


@router.get("/projects/{project_id}/sites", response_model=list[SiteRead])
def list_sites(
    db: Session = Depends(get_db), project: Project = Depends(get_owned_project)
) -> list[SiteRead]:
    sites = crud_site.get_multi_by_project(db, project_id=project.id)
    return [_site_to_read(site) for site in sites]


@router.get("/sites", response_model=list[SiteWithProject])
def list_all_sites(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[SiteWithProject]:
    """All sites across every project owned by the current user, for the dashboard map."""
    sites = crud_site.get_multi_by_owner(db, owner_id=current_user.id)
    return [
        SiteWithProject(
            id=site.id,
            project_id=site.project_id,
            name=site.name,
            area_hectares=site.area_hectares,
            geometry=wkb_to_geojson(site.geom),
            created_at=site.created_at,
            project_name=site.project.name,
        )
        for site in sites
    ]


@router.get("/sites/{site_id}", response_model=SiteRead)
def get_site(site: Site = Depends(get_owned_site)) -> SiteRead:
    return _site_to_read(site)
