from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_project
from app.crud import crud_project, crud_site
from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead, ProjectWithSites
from app.schemas.site import SiteRead
from app.utils.geo import wkb_to_geojson

router = APIRouter()


def _site_to_read(site) -> SiteRead:
    return SiteRead(
        id=site.id,
        project_id=site.project_id,
        name=site.name,
        area_hectares=site.area_hectares,
        geometry=wkb_to_geojson(site.geom),
        created_at=site.created_at,
    )


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    return crud_project.create(db, project_in=project_in, owner_id=current_user.id)


@router.get("", response_model=list[ProjectRead])
def list_projects(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Project]:
    return crud_project.get_multi_by_owner(db, owner_id=current_user.id)


@router.get("/{project_id}", response_model=ProjectWithSites)
def get_project(
    db: Session = Depends(get_db), project: Project = Depends(get_owned_project)
) -> ProjectWithSites:
    sites = crud_site.get_multi_by_project(db, project_id=project.id)
    return ProjectWithSites(
        id=project.id,
        name=project.name,
        description=project.description,
        project_type=project.project_type,
        owner_id=project.owner_id,
        created_at=project.created_at,
        sites=[_site_to_read(site) for site in sites],
    )
