/**
 * InterviewHeader
 * Props:
 *   questionNumber: number
 *   phase: "idle" | "listening" | "thinking" | "done"
 */
const PHASE_LABEL = {
    idle: "Waiting",
    listening: "Answering",
    thinking: "Evaluating",
    done: "Complete",
};

const PHASE_CLASS = {
    idle: "badge--idle",
    listening: "badge--live",
    thinking: "badge--working",
    done: "badge--done",
};

function InterviewHeader({ questionNumber, phase = "idle" }) {
    return (
        <header className="pw__titlebar" style={{ borderBottom: "none" }}>
            <span className="pw__dots">
                <span />
                <span />
                <span />
            </span>
            <span className="pw__title">InterviewHive</span>
            <span
                className="pw__meta"
                style={{ display: "flex", alignItems: "center", gap: 10 }}
            >
                Question {questionNumber}
                <span className={`badge ${PHASE_CLASS[phase]}`}>
                    <span className="badge__led" />
                    {PHASE_LABEL[phase]}
                </span>
            </span>
        </header>
    );
}

export default InterviewHeader;