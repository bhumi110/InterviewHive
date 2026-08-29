import { useEffect, useRef, useState } from "react";

/**
 * AgentRoster
 * -----------
 * Shows the four AI agents behind the interview (Manager, Judge, Evaluator,
 * Skeptic) as pixel-avatar cards, mirroring the "agent card" language from
 * the reference dashboard (avatar + name + status pill).
 *
 * Deliberately built with SVG/CSS rather than a canvas: it needs to be
 * reliable across every browser/GPU combo, and four more Pixi instances
 * would be four more places for renderer init to fail.
 *
 * Props:
 *   phase: "idle" | "listening" | "thinking" | "done"
 */

const AGENTS = [
    {
        key: "manager",
        name: "Manager",
        role: "runs the session",
        color: "#5f7fb8",
        initial: "M",
    },
    {
        key: "evaluator",
        name: "Evaluator",
        role: "scores each answer",
        color: "#4f9e6b",
        initial: "E",
    },
    {
        key: "skeptic",
        name: "Skeptic",
        role: "stress-tests your claims",
        color: "#b85f5f",
        initial: "S",
    },
    {
        key: "judge",
        name: "Judge",
        role: "delivers the verdict",
        color: "#8a5fb8",
        initial: "J",
    },
];

function AgentRoster({ phase = "idle" }) {
    const [activeIndex, setActiveIndex] = useState(-1);
    const timerRef = useRef(null);

    useEffect(() => {
        clearInterval(timerRef.current);

        if (phase !== "thinking") {
            setActiveIndex(-1);
            return;
        }

        // cycle through the panel one agent at a time, so it reads as the
        // agents taking turns deliberating rather than a generic spinner
        let i = 0;
        setActiveIndex(0);
        timerRef.current = setInterval(() => {
            i = (i + 1) % AGENTS.length;
            setActiveIndex(i);
        }, 900);

        return () => clearInterval(timerRef.current);
    }, [phase]);

    return (
        <div className="agent-grid">
            {AGENTS.map((agent, index) => {
                const isManager = agent.key === "manager";
                const isActive = phase === "thinking" && index === activeIndex;
                const isDone = phase === "done";
                const isListeningLead = phase === "listening" && isManager;

                let statusLabel = "Idle";
                let badgeClass = "badge--idle";

                if (isDone) {
                    statusLabel = "Done";
                    badgeClass = "badge--done";
                } else if (isActive) {
                    statusLabel = "Reviewing…";
                    badgeClass = "badge--working";
                } else if (phase === "thinking") {
                    statusLabel = "Standby";
                    badgeClass = "badge--idle";
                } else if (isListeningLead) {
                    statusLabel = "Watching";
                    badgeClass = "badge--live";
                }

                const cardClass = [
                    "agent-card",
                    isActive && "agent-card--working",
                    isDone && "agent-card--done",
                ]
                    .filter(Boolean)
                    .join(" ");

                return (
                    <div key={agent.key} className={cardClass}>
                        {isActive && (
                            <div className="agent-card__bubble" aria-hidden="true">
                                <span className="dot" />
                                <span className="dot" />
                                <span className="dot" />
                            </div>
                        )}

                        <div
                            className="agent-card__avatar"
                            style={{ "--agent-color": agent.color }}
                        >
                            <svg
                                viewBox="0 0 24 24"
                                width="40"
                                height="40"
                                shapeRendering="crispEdges"
                            >
                                <rect x="4" y="10" width="16" height="12" fill={agent.color} />
                                <rect x="6" y="2" width="12" height="10" fill="#e7c9a1" />
                                <rect x="6" y="2" width="12" height="4" fill="#2b2b23" />
                                <rect x="9" y="7" width="2" height="2" fill="#2b2b23" />
                                <rect x="13" y="7" width="2" height="2" fill="#2b2b23" />
                            </svg>
                            <span className="agent-card__initial">{agent.initial}</span>
                        </div>

                        <div className="agent-card__name">{agent.name}</div>
                        <div className="agent-card__role">{agent.role}</div>

                        <span className={`badge ${badgeClass}`}>
                            <span className="badge__led" />
                            {statusLabel}
                        </span>
                    </div>
                );
            })}
        </div>
    );
}

export default AgentRoster;