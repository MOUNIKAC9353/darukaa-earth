from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Polygon, mapping

from app.schemas.site import GeoJSONPolygon


def geojson_to_wkb(geometry: GeoJSONPolygon, srid: int = 4326):
    """Convert an incoming GeoJSON polygon into a PostGIS-ready WKB element."""
    polygon = Polygon(geometry.coordinates[0], holes=geometry.coordinates[1:] or None)
    return from_shape(polygon, srid=srid)


def wkb_to_geojson(geom) -> GeoJSONPolygon:
    """Convert a stored PostGIS geometry back into a GeoJSON polygon for API responses."""
    shape = to_shape(geom)
    return GeoJSONPolygon(**mapping(shape))


def polygon_area_hectares(geometry: GeoJSONPolygon) -> float:
    """Approximate area in hectares using an equal-area projection-free planar estimate.

    For production use, this should reproject to an appropriate equal-area CRS.
    Here we use a simple geodesic approximation suitable for demo purposes.
    """
    polygon = Polygon(geometry.coordinates[0])
    # Rough conversion: at the equator, 1 degree ~ 111.32 km. This is an approximation
    # intended for demo/mock data rather than survey-grade area calculations.
    degrees_to_meters = 111_320
    area_sq_degrees = polygon.area
    area_sq_meters = area_sq_degrees * (degrees_to_meters**2)
    return round(area_sq_meters / 10_000, 4)
