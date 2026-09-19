from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


def create(db: Session, project_in: ProjectCreate, owner_id: int) -> Project:
    project = Project(
        name=project_in.name,
        description=project_in.description,
        project_type=project_in.project_type,
        owner_id=owner_id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def get_multi_by_owner(db: Session, owner_id: int) -> list[Project]:
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .order_by(Project.created_at.desc())
        .all()
    )
