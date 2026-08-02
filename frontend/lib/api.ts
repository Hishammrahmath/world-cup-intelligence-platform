const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type Match = {
  match_id: number;
  date: string;
  kickoff_time_utc: string;
  stage_id: number;
  venue_id: number;
  home_team_id: number;
  away_team_id: number;
  home_score: number;
  away_score: number;
  status: string;
  result_type: string | null;
  home_xg: number;
  away_xg: number;
};

export type Team = {
  team_id: number;
  team_name: string;
  fifa_code: string;
};

export type Event = {
  event_id?: number;
  match_id?: number;
  minute: number | string;
  event_type: string;
  team_id: number;
  player_id?: number;
};

export type TeamStats = {
  match_id: number;
  team_id: number;
  possession_pct: number;
  total_shots: number;
  shots_on_target: number;
  corners: number;
  fouls: number;
  offsides: number;
  saves: number;
};

export type MomentumPoint = {
  minute: number;
  team_id: number;
  event_score: number;
  momentum_score: number;
};

export type TurningPoint = {
  start_minute: number;
  end_minute: number;
  team_id: number;
  change_size: number;
  nearby_events: Event[];
};

export type MatchSummary = {
  facts: {
    match_id: number;
    status: string;
    result_type: string | null;
    date: string;
    home_team: Team;
    away_team: Team;
    score: { home: number; away: number };
    event_count: number;
    goal_count: number;
    card_count: number;
    turning_point_count: number;
    top_stat_notes: string[];
  };
  fan_explanation: string;
  player_explanation: string;
  coach_explanation: string;
  limits: string[];
};

export type MatchDashboardData = {
  match: Match;
  teams: Team[];
  events: Event[];
  stats: TeamStats[];
  momentum: MomentumPoint[];
  turningPoints: TurningPoint[];
  summary: MatchSummary;
};

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export async function getMatchDashboard(matchId: number): Promise<MatchDashboardData> {
  const [match, teams, events, stats, momentum, turningPoints, summary] = await Promise.all([
    fetchJson<{ match: Match }>(`/matches/${matchId}`),
    fetchJson<{ teams: Team[] }>(`/matches/${matchId}/teams`),
    fetchJson<{ events: Event[] }>(`/matches/${matchId}/events`),
    fetchJson<{ stats: TeamStats[] }>(`/matches/${matchId}/stats`),
    fetchJson<{ momentum: MomentumPoint[] }>(`/matches/${matchId}/momentum`),
    fetchJson<{ turning_points: TurningPoint[] }>(`/matches/${matchId}/turning-points`),
    fetchJson<{ summary: MatchSummary }>(`/matches/${matchId}/summary`),
  ]);

  return {
    match: match.match,
    teams: teams.teams,
    events: events.events,
    stats: stats.stats,
    momentum: momentum.momentum,
    turningPoints: turningPoints.turning_points,
    summary: summary.summary,
  };
}

