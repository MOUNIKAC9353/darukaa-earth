import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { Line } from "react-chartjs-2";
import type { SiteMetric } from "../types";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export function SiteChart({ metrics }: { metrics: SiteMetric[] }) {
  const labels = metrics.map((m) => m.recorded_date);

  const data = {
    labels,
    datasets: [
      {
        label: "Carbon (tons)",
        data: metrics.map((m) => m.carbon_tons),
        borderColor: "#2f9e44",
        backgroundColor: "#2f9e4433",
        yAxisID: "y",
      },
      {
        label: "Biodiversity index",
        data: metrics.map((m) => m.biodiversity_index),
        borderColor: "#1971c2",
        backgroundColor: "#1971c233",
        yAxisID: "y",
      },
      {
        label: "NDVI",
        data: metrics.map((m) => m.ndvi),
        borderColor: "#e8590c",
        backgroundColor: "#e8590c33",
        yAxisID: "y1",
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: { mode: "index" as const, intersect: false },
    scales: {
      y: { type: "linear" as const, position: "left" as const },
      y1: {
        type: "linear" as const,
        position: "right" as const,
        min: -1,
        max: 1,
        grid: { drawOnChartArea: false },
      },
    },
  };

  return <Line data={data} options={options} />;
}
