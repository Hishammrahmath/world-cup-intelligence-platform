"use client";

import { useEffect, useMemo, useState } from "react";
import { Activity, Brain, ClipboardList, Dumbbell, Search } from "lucide-react";
import { getMatchDashboard, getMatchList, type MatchDashboardData, type MatchListItem } from "@/lib/api";
import EventTimeline from "./EventTimeline";
import MomentumChart from "./MomentumChart";
import StatsTable from "./StatsTable";
import TurningPointsPanel from "./TurningPointsPanel";

type ViewMode = "fan" | "player" | "coach";

type Props = {
  initialMatchId: number;
};

export default function MatchDashboard({ initialMatchId }: Props) {
  const [matchList, setMatchList] = useState<MatchListItem[]>([]);
  const [activeMatchId, setActiveMatchId] = useState(initialMatchId);
  const [activeMode, setActiveMode] = useState<ViewMode>("fan");
  const [data, setData] = useState<MatchDashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fromUrl = Number(new URLSearchParams(window.location.search).get("match"));
    if (Number.isInteger(fromUrl) && fromUrl > 0) {
      setActiveMatchId(fromUrl);
    }

    getMatchList()
      .then(setMatchList)
      .catch(() => setMatchList([]));
  }, []);

  useEffect(() => {
    let isCurrent = true;
    setIsLoading(true);
    setError(null);

    getMatchDashboard(activeMatchId)
      .then((dashboardData) => {
        if (isCurrent) {
          setData(dashboardData);
        }
      })
      .catch((requestError: Error) => {
        if (isCurrent) {
          setError(requestError.message);
          setData(null);
        }
      })
      .finally(() => {
        if (isCurrent) {
          setIsLoading(false);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, [activeMatchId]);

  const teamsById = useMemo(() => {
    return new Map(data?.teams.map((team) => [team.team_id, team]) ?? []);
  }, [data]);

  const homeTeam = data ? teamsById.get(data.match.home_team_id) : null;
  const awayTeam = data ? teamsById.get(data.match.away_team_id) : null;

  function selectMatch(matchId: number) {
    setActiveMatchId(matchId);
    const url = new URL(window.location.href);
    url.searchParams.set("match", String(matchId));
    window.history.replaceState(null, "", url);
  }

  const explanation = data ? getModeExplanation(activeMode, data) : "";

  return (
    <main className="appShell">
      <section className="topBar">
        <div>
          <p className="eyebrow">MatchIQ · FIFA World Cup 2026</p>
          <h1>Match Momentum Dashboard</h1>
          <p className="tagline">
            Event-weighted momentum, turning points, and fact-only explanations for all 104 matches.
          </p>
        </div>
        <label className="matchSearch">
          <Search size={18} />
          <select
            value={activeMatchId}
            onChange={(event) => selectMatch(Number(event.target.value))}
            aria-label="Choose a match"
          >
            {matchList.length === 0 && <option value={activeMatchId}>Match {activeMatchId}</option>}
            {matchList.map((item) => (
              <option key={item.match_id} value={item.match_id}>
                {formatMatchOption(item)}
              </option>
            ))}
          </select>
        </label>
      </section>

      {error && <div className="statusBanner error">{error}</div>}
      {isLoading && <div className="statusBanner">Loading match intelligence...</div>}

      {data && homeTeam && awayTeam && (
        <>
          <section className="matchHeader">
            <div className="teamBlock">
              <span>{homeTeam.fifa_code}</span>
              <strong>{homeTeam.team_name}</strong>
            </div>
            <div className="scoreBlock">
              <div className="scoreLine">
                {data.match.home_score} - {data.match.away_score}
              </div>
              <div className="matchMeta">
                Match {data.match.match_id} · {data.match.date} · {data.match.status}
              </div>
            </div>
            <div className="teamBlock alignRight">
              <span>{awayTeam.fifa_code}</span>
              <strong>{awayTeam.team_name}</strong>
            </div>
          </section>

          <section className="modeTabs" aria-label="View mode">
            <ModeButton mode="fan" activeMode={activeMode} setActiveMode={setActiveMode} />
            <ModeButton mode="player" activeMode={activeMode} setActiveMode={setActiveMode} />
            <ModeButton mode="coach" activeMode={activeMode} setActiveMode={setActiveMode} />
          </section>

          <section className="explanationPanel">
            <div className="panelTitle">
              <Brain size={18} />
              <h2>{modeLabel(activeMode)} Explanation</h2>
            </div>
            <p>{explanation}</p>
          </section>

          <section className="dashboardGrid">
            <div className="widePanel">
              <div className="panelTitle">
                <Activity size={18} />
                <h2>Momentum</h2>
              </div>
              <MomentumChart momentum={data.momentum} teamsById={teamsById} />
            </div>

            <StatsTable stats={data.stats} teamsById={teamsById} />
            <TurningPointsPanel turningPoints={data.turningPoints} teamsById={teamsById} />

            <div className="widePanel">
              <div className="panelTitle">
                <ClipboardList size={18} />
                <h2>Event Timeline</h2>
              </div>
              <EventTimeline events={data.events} teamsById={teamsById} />
            </div>
          </section>
        </>
      )}
    </main>
  );
}

function ModeButton({
  mode,
  activeMode,
  setActiveMode,
}: {
  mode: ViewMode;
  activeMode: ViewMode;
  setActiveMode: (mode: ViewMode) => void;
}) {
  const Icon = mode === "fan" ? Activity : mode === "player" ? Dumbbell : ClipboardList;

  return (
    <button
      className={activeMode === mode ? "active" : ""}
      onClick={() => setActiveMode(mode)}
      type="button"
    >
      <Icon size={16} />
      {modeLabel(mode)}
    </button>
  );
}

function modeLabel(mode: ViewMode) {
  if (mode === "fan") return "Fan View";
  if (mode === "player") return "Player View";
  return "Coach View";
}

function getModeExplanation(mode: ViewMode, data: MatchDashboardData) {
  if (mode === "fan") return data.summary.fan_explanation;
  if (mode === "player") return data.summary.player_explanation;
  return data.summary.coach_explanation;
}


function formatMatchOption(item: MatchListItem) {
  if (!item.home_team || !item.away_team) {
    return `Match ${item.match_id} · ${item.date}`;
  }

  return `#${item.match_id} · ${item.home_team} ${item.home_score}–${item.away_score} ${item.away_team} · ${item.date}`;
}
