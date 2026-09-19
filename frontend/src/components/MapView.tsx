import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import "mapbox-gl/dist/mapbox-gl.css";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import type { GeoJSONPolygon, Site } from "../types";

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

interface MapViewProps {
  sites: Site[];
  onSiteDrawn?: (geometry: GeoJSONPolygon) => void;
  onSiteClick?: (siteId: number) => void;
  focusSiteId?: number;
}

const SITES_SOURCE_ID = "sites";

export function MapView({ sites, onSiteDrawn, onSiteClick, focusSiteId }: MapViewProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const drawRef = useRef<MapboxDraw | null>(null);
  const onSiteClickRef = useRef(onSiteClick);

  useEffect(() => {
    onSiteClickRef.current = onSiteClick;
  }, [onSiteClick]);

  // Initialize the map once.
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: [78.9629, 20.5937],
      zoom: 4,
    });
    map.addControl(new mapboxgl.NavigationControl(), "top-right");

    map.on("load", () => {
      map.addSource(SITES_SOURCE_ID, {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addLayer({
        id: `${SITES_SOURCE_ID}-fill`,
        type: "fill",
        source: SITES_SOURCE_ID,
        paint: { "fill-color": "#2f9e44", "fill-opacity": 0.35 },
      });
      map.addLayer({
        id: `${SITES_SOURCE_ID}-outline`,
        type: "line",
        source: SITES_SOURCE_ID,
        paint: { "line-color": "#2f9e44", "line-width": 2 },
      });

      map.on("click", `${SITES_SOURCE_ID}-fill`, (e) => {
        const siteId = e.features?.[0]?.properties?.id;
        if (siteId != null) onSiteClickRef.current?.(Number(siteId));
      });
      map.on("mouseenter", `${SITES_SOURCE_ID}-fill`, () => {
        map.getCanvas().style.cursor = onSiteClickRef.current ? "pointer" : "";
      });
      map.on("mouseleave", `${SITES_SOURCE_ID}-fill`, () => {
        map.getCanvas().style.cursor = "";
      });
    });


    if (onSiteDrawn) {
      const draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: { polygon: true, trash: true },
      });
      map.addControl(draw, "top-left");
      drawRef.current = draw;

      map.on("draw.create", (e: { features: GeoJSON.Feature[] }) => {
        const feature = e.features[0];
        if (feature?.geometry.type === "Polygon") {
          onSiteDrawn(feature.geometry as GeoJSONPolygon);
          draw.deleteAll();
        }
      });
    }

    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Keep the rendered site polygons and camera in sync with props.
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    const applyData = () => {
      const source = map.getSource(SITES_SOURCE_ID) as mapboxgl.GeoJSONSource | undefined;
      if (!source) return;

      const features = sites.map((site) => ({
        type: "Feature" as const,
        properties: { id: site.id, name: site.name },
        geometry: site.geometry,
      }));
      source.setData({ type: "FeatureCollection", features });

      if (features.length > 0) {
        const bounds = new mapboxgl.LngLatBounds();
        for (const feature of features) {
          for (const ring of feature.geometry.coordinates) {
            for (const [lng, lat] of ring) bounds.extend([lng, lat]);
          }
        }
        map.fitBounds(bounds, { padding: 40, maxZoom: 14, duration: 500 });
      }
    };

    if (map.isStyleLoaded()) applyData();
    else map.once("load", applyData);
  }, [sites, focusSiteId]);

  return <div ref={containerRef} className="map-container" />;
}
