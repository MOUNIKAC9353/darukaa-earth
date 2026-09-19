import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useParams } from "react-router-dom";
import { apiClient } from "../api/client";
import { SiteChart } from "../components/SiteChart";
import type { Site, SiteMetric } from "../types";
import { extractErrorMessage } from "../utils/errors";

export function SitePage() {
  const { siteId } = useParams<{ siteId: string }>();
  const [site, setSite] = useState<Site | null>(null);
  const [metrics, setMetrics] = useState<SiteMetric[]>([]);
  const [recordedDate, setRecordedDate] = useState("");
  const [carbonTons, setCarbonTons] = useState("");
  const [biodiversityIndex, setBiodiversityIndex] = useState("");
  const [ndvi, setNdvi] = useState("");
  const [error, setError] = useState<string | null>(null);

  function loadData() {
    apiClient.get<Site>(`/sites/${siteId}`).then((res) => setSite(res.data));
    apiClient.get<SiteMetric[]>(`/sites/${siteId}/metrics`).then((res) => setMetrics(res.data));
  }

  useEffect(loadData, [siteId]);

  async function handleAddMetric(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await apiClient.post(`/sites/${siteId}/metrics`, {
        recorded_date: recordedDate,
        carbon_tons: Number(carbonTons),
        biodiversity_index: Number(biodiversityIndex),
        ndvi: Number(ndvi),
      });
      setRecordedDate("");
      setCarbonTons("");
      setBiodiversityIndex("");
      setNdvi("");
      loadData();
    } catch (err) {
      setError(extractErrorMessage(err, "Could not add observation."));
    }
  }

  if (!site) return <p className="loading">Loading site...</p>;

  return (
    <div>
      <h1>{site.name}</h1>
      {site.area_hectares && <p>{site.area_hectares.toFixed(2)} hectares</p>}

      <h2>Performance over time</h2>
      {metrics.length > 0 ? (
        <SiteChart metrics={metrics} />
      ) : (
        <p>No observations recorded yet.</p>
      )}

      <h2>Add observation</h2>
      <form className="inline-form" onSubmit={handleAddMetric}>
        <input
          type="date"
          value={recordedDate}
          onChange={(e) => setRecordedDate(e.target.value)}
          required
        />
        <input
          type="number"
          step="0.01"
          placeholder="Carbon (tons)"
          value={carbonTons}
          onChange={(e) => setCarbonTons(e.target.value)}
          required
        />
        <input
          type="number"
          step="0.01"
          placeholder="Biodiversity index"
          value={biodiversityIndex}
          onChange={(e) => setBiodiversityIndex(e.target.value)}
          required
        />
        <input
          type="number"
          step="0.001"
          placeholder="NDVI"
          value={ndvi}
          onChange={(e) => setNdvi(e.target.value)}
          required
        />
        <button type="submit">Add</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
