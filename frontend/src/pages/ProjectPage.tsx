import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { apiClient } from "../api/client";
import { MapView } from "../components/MapView";
import type { GeoJSONPolygon, ProjectWithSites } from "../types";
import { extractErrorMessage } from "../utils/errors";

export function ProjectPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<ProjectWithSites | null>(null);
  const [siteName, setSiteName] = useState("");
  const [pendingGeometry, setPendingGeometry] = useState<GeoJSONPolygon | null>(null);
  const [error, setError] = useState<string | null>(null);

  function loadProject() {
    apiClient.get<ProjectWithSites>(`/projects/${projectId}`).then((res) => setProject(res.data));
  }

  useEffect(loadProject, [projectId]);

  async function handleCreateSite() {
    if (!pendingGeometry || !siteName.trim()) return;
    setError(null);
    try {
      await apiClient.post(`/projects/${projectId}/sites`, {
        name: siteName,
        geometry: pendingGeometry,
      });
      setSiteName("");
      setPendingGeometry(null);
      loadProject();
    } catch (err) {
      setError(extractErrorMessage(err, "Could not create site."));
    }
  }

  if (!project) return <p className="loading">Loading project...</p>;

  return (
    <div>
      <h1>{project.name}</h1>
      {project.description && <p>{project.description}</p>}

      <MapView
        sites={project.sites}
        onSiteDrawn={setPendingGeometry}
        onSiteClick={(siteId) => navigate(`/sites/${siteId}`)}
      />

      {pendingGeometry && (
        <div className="inline-form">
          <input
            placeholder="New site name"
            value={siteName}
            onChange={(e) => setSiteName(e.target.value)}
          />
          <button onClick={handleCreateSite}>Save site</button>
          <button onClick={() => setPendingGeometry(null)}>Cancel</button>
        </div>
      )}
      {error && <p className="error">{error}</p>}

      <h2>Sites</h2>
      <ul className="site-list">
        {project.sites.map((site) => (
          <li key={site.id}>
            <Link to={`/sites/${site.id}`}>{site.name}</Link>
            {site.area_hectares && <span> — {site.area_hectares.toFixed(2)} ha</span>}
          </li>
        ))}
        {project.sites.length === 0 && (
          <li>Draw a polygon on the map to add the first site.</li>
        )}
      </ul>
    </div>
  );
}
