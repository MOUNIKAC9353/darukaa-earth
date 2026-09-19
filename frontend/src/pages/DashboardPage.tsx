import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../api/client";
import { MapView } from "../components/MapView";
import type { Project, SiteWithProject } from "../types";
import { extractErrorMessage } from "../utils/errors";

export function DashboardPage() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [sites, setSites] = useState<SiteWithProject[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [projectType, setProjectType] = useState("carbon");
  const [error, setError] = useState<string | null>(null);

  function loadProjects() {
    setIsLoading(true);
    apiClient
      .get<Project[]>("/projects")
      .then((res) => setProjects(res.data))
      .finally(() => setIsLoading(false));
  }

  function loadSites() {
    apiClient.get<SiteWithProject[]>("/sites").then((res) => setSites(res.data));
  }

  useEffect(() => {
    loadProjects();
    loadSites();
  }, []);

  async function handleCreate(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await apiClient.post("/projects", {
        name,
        description: description || null,
        project_type: projectType,
      });
      setName("");
      setDescription("");
      loadProjects();
    } catch (err) {
      setError(extractErrorMessage(err, "Could not create project."));
    }
  }

  return (
    <div>
      <h1>Projects</h1>

      <form className="inline-form" onSubmit={handleCreate}>
        <input
          placeholder="Project name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select value={projectType} onChange={(e) => setProjectType(e.target.value)}>
          <option value="carbon">Carbon</option>
          <option value="biodiversity">Biodiversity</option>
        </select>
        <button type="submit">Create project</button>
      </form>
      {error && <p className="error">{error}</p>}

      {sites.length > 0 && (
        <>
          <h2>All sites</h2>
          <MapView sites={sites} onSiteClick={(siteId) => navigate(`/sites/${siteId}`)} />
        </>
      )}

      {isLoading ? (
        <p className="loading">Loading projects...</p>
      ) : (
        <div className="card-grid">
          {projects.map((project) => (
            <Link key={project.id} to={`/projects/${project.id}`} className="card">
              <h2>{project.name}</h2>
              <p className="badge">{project.project_type}</p>
              {project.description && <p>{project.description}</p>}
            </Link>
          ))}
          {projects.length === 0 && <p>No projects yet — create one above.</p>}
        </div>
      )}
    </div>
  );
}
