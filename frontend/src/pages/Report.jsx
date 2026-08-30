import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getReport } from "../services/api";

import PixelWindow from "../pixi/pixelWindow";
import InterviewRoomScene from "../pixi/Interviewroomscene";
import AgentRoster from "../pixi/agentRoster";
import logo from "../assets/logo.png";


function ScoreBar({ label, value }) {
    const segments = 10;
    const filled = Math.round(Number(value) || 0);

    return (
        <div className="bar-row">
            <span>{label}</span>
            <span className="bar-track">
                {Array.from({ length: segments }).map((_, i) => (
                    <span
                        key={i}
                        className={`bar-track__segment ${
                            i < filled ? "bar-track__segment--filled" : ""
                        }`}
                    />
                ))}
            </span>
            <span className="bar-value">{value}/10</span>
        </div>
    );
}

function Report() {
    const navigate = useNavigate();

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadReport() {
            const session = sessionStorage.getItem("interview_session");

            if (!session) {
                setError("No interview session found.");
                setLoading(false);
                return;
            }

            const sessionData = JSON.parse(session);
            const sessionId = sessionData.sessionId;

            if (!sessionId) {
                setError("Invalid interview session.");
                setLoading(false);
                return;
            }

            try {
                const data = await getReport(sessionId);
                setReport(data.report);
            } catch (err) {
                console.error("Report loading error:", err);
                setError(
                    err.response?.data?.detail || "Could not load interview report."
                );
            } finally {
                setLoading(false);
            }
        }

        loadReport();
    }, []);

    if (loading) {
        return (
            <div className="app-shell">
                <div className="app-shell__inner">
                    <PixelWindow title="SESSION_REPORT" meta="compiling…" tight>
                        <InterviewRoomScene phase="thinking" height={150} />
                    </PixelWindow>
                    <PixelWindow title="STATUS">
                        <div className="terminal-block">
                            <div className="terminal-line">
                                <span className="prompt">&gt;</span>
                                <span>Generating your report…</span>
                            </div>
                            <div className="terminal-line">
                                <span className="prompt">&gt;</span>
                                <span>Analysing your interview performance.</span>
                            </div>
                        </div>
                    </PixelWindow>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="app-shell">
                <div className="app-shell__inner">
                    <PixelWindow title="ERROR">
                        <h1 style={{ fontSize: 16, marginBottom: 10 }}>
                            Unable to load report
                        </h1>
                        <p className="error-text" style={{ marginBottom: 16 }}>
                            {error}
                        </p>
                        <button
                            className="btn-pixel"
                            onClick={() => navigate("/setup")}
                        >
                            Start new interview →
                        </button>
                    </PixelWindow>
                </div>
            </div>
        );
    }

    if (!report) return null;

    return (
        <div className="app-shell">
            <div className="app-topbar">
                <span className="app-topbar__brand">
                                    <img
                                        src={logo}
                                        alt="InterviewHive"
                                        className="app-topbar__logo"
                                    />
                                    <span>INTERVIEWHIVE</span>
                                </span>
                <span className="app-topbar__meta">session report</span>
            </div>

            <div className="app-shell__inner">
                <PixelWindow title="SESSION_REPORT" meta="complete" tight>
                    <InterviewRoomScene phase="done" height={150} />
                </PixelWindow>
                

                <PixelWindow title="AGENT_PANEL" meta="4 agents · signed off">
                    <AgentRoster phase="done" />
                </PixelWindow>

                <PixelWindow title="OVERALL_SCORE">
                    <div
                        style={{
                            display: "flex",
                            alignItems: "baseline",
                            gap: 16,
                            marginBottom: 12,
                        }}
                    >
                        <h2 style={{ fontSize: 34, color: "var(--amber-dim)" }}>
                            {report.overall_score}
                            <span style={{ fontSize: 16, color: "var(--ink-dim)" }}>
                                /10
                            </span>
                        </h2>
                        <span className="badge badge--done">
                            <span className="badge__led" />
                            Session complete
                        </span>
                    </div>
                    <p
                        style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: 13.5,
                            lineHeight: 1.6,
                            color: "var(--ink-dim)",
                            margin: 0,
                        }}
                    >
                        {report.summary}
                    </p>
                </PixelWindow>

                <PixelWindow title="PERFORMANCE">
                    <ScoreBar label="Technical" value={report.technical_score} />
                    <ScoreBar
                        label="Problem solving"
                        value={report.problem_solving_score}
                    />
                    <ScoreBar
                        label="Communication"
                        value={report.communication_score}
                    />
                    <ScoreBar label="Confidence" value={report.confidence_score} />
                    <ScoreBar label="Depth" value={report.depth_score} />
                </PixelWindow>

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns: "1fr 1fr",
                        gap: 20,
                    }}
                >
                    <PixelWindow title="STRENGTHS">
                        <ul className="pixel-list pixel-list--pos">
                            {report.strengths.map((strength, index) => (
                                <li key={index}>{strength}</li>
                            ))}
                        </ul>
                    </PixelWindow>

                    <PixelWindow title="WEAKNESSES">
                        <ul className="pixel-list pixel-list--neg">
                            {report.weaknesses.map((weakness, index) => (
                                <li key={index}>{weakness}</li>
                            ))}
                        </ul>
                    </PixelWindow>
                </div>

                {report.red_flags?.length > 0 && (
                    <PixelWindow title="RED_FLAGS" meta="review">
                        <ul className="pixel-list pixel-list--flag">
                            {report.red_flags.map((flag, index) => (
                                <li key={index}>{flag}</li>
                            ))}
                        </ul>
                    </PixelWindow>
                )}

                <PixelWindow title="RECOMMENDED_TOPICS">
                    <ul className="pixel-list pixel-list--topic">
                        {report.recommended_topics.map((topic, index) => (
                            <li key={index}>{topic}</li>
                        ))}
                    </ul>
                </PixelWindow>

                <button
                    className="btn-pixel btn-pixel--full"
                    onClick={() => navigate("/setup")}
                >
                    Practice again →
                </button>
            </div>
        </div>
    );
}

export default Report;