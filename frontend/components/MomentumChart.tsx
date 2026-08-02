"use client";

import dynamic from "next/dynamic";
import type { Layout, Data } from "plotly.js";
import type { MomentumPoint, Team } from "@/lib/api";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

type Props = {
  momentum: MomentumPoint[];
  teamsById: Map<number, Team>;
};

export default function MomentumChart({ momentum, teamsById }: Props) {
  const traces: Data[] = Array.from(teamsById.values()).map((team, index) => {
    const teamMomentum = momentum.filter((point) => point.team_id === team.team_id);

    return {
      x: teamMomentum.map((point) => point.minute),
      y: teamMomentum.map((point) => point.momentum_score),
      type: "scatter",
      mode: "lines",
      name: team.fifa_code,
      line: {
        width: 3,
        color: index === 0 ? "#0f766e" : "#c2410c",
      },
    };
  });

  const layout: Partial<Layout> = {
    autosize: true,
    height: 360,
    margin: { l: 44, r: 20, t: 12, b: 42 },
    paper_bgcolor: "transparent",
    plot_bgcolor: "transparent",
    font: { color: "#1f2937" },
    xaxis: { title: { text: "Minute" }, gridcolor: "#e5e7eb" },
    yaxis: { title: { text: "Momentum score" }, gridcolor: "#e5e7eb" },
    legend: { orientation: "h", y: -0.22 },
  };

  return (
    <div className="chartFrame">
      <Plot data={traces} layout={layout} config={{ displayModeBar: false, responsive: true }} />
    </div>
  );
}

