import type { Event, Team } from "@/lib/api";

type Props = {
  events: Event[];
  teamsById: Map<number, Team>;
};

export default function EventTimeline({ events, teamsById }: Props) {
  if (events.length === 0) {
    return <p className="emptyState">No tracked events are available for this match.</p>;
  }

  return (
    <div className="timeline">
      {events.map((event, index) => {
        const team = teamsById.get(event.team_id);
        return (
          <div className="timelineRow" key={`${event.event_id ?? index}-${event.minute}`}>
            <div className="minuteBadge">{event.minute}'</div>
            <div>
              <strong>{event.event_type}</strong>
              <span>{team ? team.team_name : `Team ${event.team_id}`}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

