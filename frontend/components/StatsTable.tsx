import { Table2 } from "lucide-react";
import type { Team, TeamStats } from "@/lib/api";

type Props = {
  stats: TeamStats[];
  teamsById: Map<number, Team>;
};

const STAT_COLUMNS: Array<{ key: keyof TeamStats; label: string }> = [
  { key: "possession_pct", label: "Poss." },
  { key: "total_shots", label: "Shots" },
  { key: "shots_on_target", label: "SOT" },
  { key: "corners", label: "Corners" },
  { key: "fouls", label: "Fouls" },
  { key: "saves", label: "Saves" },
];

export default function StatsTable({ stats, teamsById }: Props) {
  return (
    <section className="panel">
      <div className="panelTitle">
        <Table2 size={18} />
        <h2>Team Stats</h2>
      </div>
      {stats.length === 0 ? (
        <p className="emptyState">No team stats are available for this match.</p>
      ) : (
        <div className="tableWrap">
          <table>
            <thead>
              <tr>
                <th>Team</th>
                {STAT_COLUMNS.map((column) => (
                  <th key={column.key}>{column.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {stats.map((row) => {
                const team = teamsById.get(row.team_id);
                return (
                  <tr key={row.team_id}>
                    <td>{team?.fifa_code ?? row.team_id}</td>
                    {STAT_COLUMNS.map((column) => (
                      <td key={column.key}>{row[column.key]}</td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

