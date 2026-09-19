import random
from datetime import date, timedelta

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.project import Project
from app.models.site import Site
from app.models.site_metric import SiteMetric
from app.models.user import User
from app.schemas.site import GeoJSONPolygon
from app.utils.geo import geojson_to_wkb, polygon_area_hectares

# Mock demo data. We use synthetic polygons and randomized-but-plausible metric
# trends (instead of a real satellite dataset) so the app can be exercised end
# to end without requiring access to a licensed geospatial data provider.
DEMO_SITES = [
    {
        "name": "Nandurbar Agroforestry Site",
        "coordinates": [
            [
                (74.240, 21.370),
                (74.250, 21.370),
                (74.250, 21.380),
                (74.240, 21.380),
                (74.240, 21.370),
            ]
        ],
    },
    {
        "name": "Western Ghats Restoration Plot",
        "coordinates": [
            [
                (73.800, 18.500),
                (73.815, 18.500),
                (73.815, 18.512),
                (73.800, 18.512),
                (73.800, 18.500),
            ]
        ],
    },
    {
        "name": "Sundarbans Mangrove Belt",
        "coordinates": [
            [
                (88.900, 21.950),
                (88.920, 21.950),
                (88.920, 21.965),
                (88.900, 21.965),
                (88.900, 21.950),
            ]
        ],
    },
]


def seed(db: Session) -> None:
    db.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    db.commit()

    user = db.query(User).filter(User.email == "admin@darukaa.earth").first()
    if not user:
        user = User(
            email="admin@darukaa.earth",
            full_name="Demo Administrator",
            hashed_password=get_password_hash("admin@123"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    project = db.query(Project).filter(Project.name == "Maharashtra Carbon Corridor").first()
    if not project:
        project = Project(
            name="Maharashtra Carbon Corridor",
            description="A multi-site reforestation and agroforestry carbon project.",
            project_type="carbon",
            owner_id=user.id,
        )
        db.add(project)
        db.commit()
        db.refresh(project)

    if db.query(Site).filter(Site.project_id == project.id).count() == 0:
        for demo_site in DEMO_SITES:
            geometry = GeoJSONPolygon(type="Polygon", coordinates=demo_site["coordinates"])
            site = Site(
                name=demo_site["name"],
                project_id=project.id,
                geom=geojson_to_wkb(geometry),
                area_hectares=polygon_area_hectares(geometry),
            )
            db.add(site)
            db.commit()
            db.refresh(site)

            start = date.today() - timedelta(days=180)
            carbon = random.uniform(50, 80)
            biodiversity = random.uniform(40, 60)
            ndvi = random.uniform(0.3, 0.5)
            for week in range(26):
                carbon += random.uniform(0.5, 2.0)
                biodiversity += random.uniform(-1.0, 1.5)
                ndvi = max(-1.0, min(1.0, ndvi + random.uniform(-0.02, 0.03)))
                db.add(
                    SiteMetric(
                        site_id=site.id,
                        recorded_date=start + timedelta(weeks=week),
                        carbon_tons=round(carbon, 2),
                        biodiversity_index=round(max(0.0, min(100.0, biodiversity)), 2),
                        ndvi=round(ndvi, 3),
                    )
                )
            db.commit()

    print("Seed complete. Demo login: admin@darukaa.earth / changeme123")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed(session)
    finally:
        session.close()
