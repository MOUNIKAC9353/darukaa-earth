# Import all models here so Alembic's autogenerate can discover them.
from app.db.base_class import Base  # noqa: F401
from app.models.project import Project  # noqa: F401
from app.models.site import Site  # noqa: F401
from app.models.site_metric import SiteMetric  # noqa: F401
from app.models.user import User  # noqa: F401
