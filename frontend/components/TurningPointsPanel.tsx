import { GitBranch } from "lucide-react";
import type { Team, TurningPoint } from "@/lib/api";

type Props = {
  turningPoints: TurningPoint[];
  teamsById: Map<number, Team>;
};

export default function TurningPointsPanel({ turningPoints, teamsById }: Props) {
  return (
    <section className="panel">
      <div className="panelTitle">
        <GitBranch size={18} />
        <h2>Turning Points</h2>
      </div>
      {turningPoints.length === 0 ? (
        <p className="emptyState">No sustained momentum shifts were detected.</p>
      ) : (
        <div className="turningList">
          {turningPoints.slice(0, 6).map((point) => {
            const team = teamsById.get(point.team_id);
            const nearbyEvents = point.nearby_events.map((event) => event.event_type).join(", ");

            return (
              <article className="turningItem" key={`${point.team_id}-${point.start_minute}-${point.end_minute}`}>
                <div>
                  <strong>
                    {point.start_minute}'-{point.end_minute}'
                  </strong>
                  <span>{team?.team_name ?? `Team ${point.team_id}`}</span>
                </div>
                <p>Momentum increased by {point.change_size.toFixed(1)} points.</p>
                {nearbyEvents && <small>Nearby events: {nearbyEvents}</small>}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}

