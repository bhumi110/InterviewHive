/**
 * AnswerInput
 * Props:
 *   value: string
 *   onChange: (value: string) => void
 *   onSubmit: () => void
 *   loading: boolean
 */
function AnswerInput({ value, onChange, onSubmit, loading }) {
    function handleKeyDown(event) {
        // Cmd/Ctrl + Enter submits, like a terminal
        if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
            event.preventDefault();
            if (!loading && value.trim()) onSubmit();
        }
    }

    return (
        <div>
            <label className="field-label" htmlFor="answer-box">
                your_answer:
            </label>

            <textarea
                id="answer-box"
                className="input-pixel"
                value={value}
                onChange={(event) => onChange(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your answer here…"
                rows={8}
                disabled={loading}
            />

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginTop: 12,
                }}
            >
                <span style={{ fontSize: 11, color: "var(--ink-dim)" }}>
                    ⌘/Ctrl + Enter to submit
                </span>

                <button
                    type="button"
                    className="btn-pixel"
                    onClick={onSubmit}
                    disabled={loading || !value.trim()}
                >
                    {loading ? "Evaluating…" : "Submit answer →"}
                </button>
            </div>
        </div>
    );
}

export default AnswerInput;