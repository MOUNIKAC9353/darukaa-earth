export interface GeoJSONPolygon {
  type: "Polygon";
  coordinates: number[][][];
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface Project {
  id: number;
  name: string;
  description: string | null;
  project_type: string;
  owner_id: number;
  created_at: string;
}

export interface Site {
  id: number;
  project_id: number;
  name: string;
  area_hectares: number | null;
  geometry: GeoJSONPolygon;
  created_at: string;
}

export interface ProjectWithSites extends Project {
  sites: Site[];
}

export interface SiteWithProject extends Site {
  project_name: string;
}

export interface SiteMetric {
  id: number;
  site_id: number;
  recorded_date: string;
  carbon_tons: number;
  biodiversity_index: number;
  ndvi: number;
  created_at: string;
}
