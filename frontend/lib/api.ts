// When NEXT_PUBLIC_API_BASE_URL is set, the dashboard calls the FastAPI backend.
// Otherwise it reads the static JSON exported by backend/scripts/export_static.py.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

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

export type MatchListItem = {
  match_id: number;
  date: string;
  home_team: string | null;
  home_code: string | null;
  away_team: string | null;
  away_code: string | null;
  home_score: number;
  away_score: number;
  turning_point_count: number;
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

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { cache: API_BASE_URL ? "no-store" : "force-cache" });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export async function getMatchList(): Promise<MatchListItem[]> {
  if (!API_BASE_URL) {
    const data = await fetchJson<{ matches: MatchListItem[] }>("/data/matches.json");
    return data.matches;
  }

  const { matches } = await fetchJson<{ matches: Match[] }>(`${API_BASE_URL}/matches`);
  return matches.map((match) => ({
    match_id: match.match_id,
    date: match.date,
    home_team: null,
    home_code: null,
    away_team: null,
    away_code: null,
    home_score: match.home_score,
    away_score: match.away_score,
    turning_point_count: 0,
  }));
}

export async function getMatchDashboard(matchId: number): Promise<MatchDashboardData> {
  if (!API_BASE_URL) {
    const data = await fetchJson<{
      match: Match;
      teams: Team[];
      events: Event[];
      stats: TeamStats[];
      momentum: MomentumPoint[];
      turning_points: TurningPoint[];
      summary: MatchSummary;
    }>(`/data/matches/${matchId}.json`);

    return {
      match: data.match,
      teams: data.teams,
      events: data.events,
      stats: data.stats,
      momentum: data.momentum,
      turningPoints: data.turning_points,
      summary: data.summary,
    };
  }

  const [match, teams, events, stats, momentum, turningPoints, summary] = await Promise.all([
    fetchJson<{ match: Match }>(`${API_BASE_URL}/matches/${matchId}`),
    fetchJson<{ teams: Team[] }>(`${API_BASE_URL}/matches/${matchId}/teams`),
    fetchJson<{ events: Event[] }>(`${API_BASE_URL}/matches/${matchId}/events`),
    fetchJson<{ stats: TeamStats[] }>(`${API_BASE_URL}/matches/${matchId}/stats`),
    fetchJson<{ momentum: MomentumPoint[] }>(`${API_BASE_URL}/matches/${matchId}/momentum`),
    fetchJson<{ turning_points: TurningPoint[] }>(`${API_BASE_URL}/matches/${matchId}/turning-points`),
    fetchJson<{ summary: MatchSummary }>(`${API_BASE_URL}/matches/${matchId}/summary`),
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

