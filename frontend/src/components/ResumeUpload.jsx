import { useRef } from "react";

/**
 * ResumeUpload
 * Props:
 *   file: File | null
 *   loading: boolean
 *   candidateProfile: object | null
 *   onSelect: (file: File) => void
 */
function ResumeUpload({ file, loading, candidateProfile, onSelect }) {
    const inputRef = useRef(null);

    const zoneClass = [
        "dropzone",
        loading && "dropzone--active",
        candidateProfile && !loading && "dropzone--done",
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div className={zoneClass}>
            <input
                ref={inputRef}
                type="file"
                accept=".pdf"
                style={{ display: "none" }}
                onChange={(event) => onSelect(event.target.files[0])}
            />

            <button
                type="button"
                className="btn-pixel btn-pixel--ghost"
                onClick={() => inputRef.current?.click()}
                disabled={loading}
            >
                {file ? "Choose a different file" : "Choose resume.pdf"}
            </button>

            {file && <span className="file-chip">{file.name}</span>}

            {loading && (
                <span className="badge badge--working">
                    <span className="badge__led" />
                    Analysing resume…
                </span>
            )}

            {candidateProfile && !loading && (
                <span className="badge badge--done">
                    <span className="badge__led" />
                    Resume parsed
                </span>
            )}

            {!file && !loading && (
                <p style={{ margin: 0, fontSize: 12, color: "var(--ink-dim)" }}>
                    PDF only. We read your experience to tailor the questions.
                </p>
            )}
        </div>
    );
}

export default ResumeUpload;