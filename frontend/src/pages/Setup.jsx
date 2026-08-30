import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { parseResume, startInterview } from "../services/api";

import PixelWindow from "../pixi/pixelWindow";
import ResumeUpload from "../components/ResumeUpload";
import RoleSelector from "../components/RoleSelector";
import logo from "../assets/logo.png";


function Setup() {
    const navigate = useNavigate();

    const [file, setFile] = useState(null);
    const [candidateProfile, setCandidateProfile] = useState(null);
    const [targetRole, setTargetRole] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleResumeUpload(selectedFile) {
        if (!selectedFile) return;

        setFile(selectedFile);
        setError("");
        setLoading(true);

        try {
            const data = await parseResume(selectedFile);

            console.log("FULL RESUME RESPONSE:", data);

            setCandidateProfile(data.candidate_profile || data);
        } catch (err) {
            console.error(err);

            setError("Could not analyse your resume.");
            setCandidateProfile(null);
        } finally {
            setLoading(false);
        }
    }

    async function handleStartInterview() {
        if (!candidateProfile) {
            setError("Please upload your resume first.");
            return;
        }

        if (!targetRole.trim()) {
            setError("Please enter your target role.");
            return;
        }

        setError("");
        setLoading(true);

        try {
            const data = await startInterview(candidateProfile, targetRole);
            console.log("SESSION ID:", data.session_id);

            /*
             * Store session information temporarily.
             * No login or permanent user storage.
             */
            sessionStorage.setItem(
                "interview_session",
                JSON.stringify({
                    sessionId: data.session_id,
                    candidateProfile,
                    targetRole,
                    question: data.question,
                    interviewerMessage: data.interviewer_message,
                })
            );

            navigate("/interview", {
                state: {
                    sessionId: data.session_id,
                    question: data.question,
                    interviewerMessage: data.interviewer_message,
                },
            });
        } catch (err) {
            console.error("Start interview failed:", err);

            const message =
                err.response?.data?.detail || "Could not start the interview.";

            setError(message);
            setCandidateProfile(null);
        } finally {
            setLoading(false);
        }
    }

    const ready = Boolean(candidateProfile) && targetRole.trim().length > 0;

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
                <span className="app-topbar__meta">setup · step 1 of 1</span>
            </div>

            <div className="app-shell__inner">
                <PixelWindow title="SETUP.exe" meta="configure session">
                    <div className="eyebrow">brief</div>
                    <h1 style={{ fontSize: 18, marginBottom: 6 }}>
                        Set up your interview
                    </h1>
                    <p
                        style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: 13,
                            color: "var(--ink-dim)",
                            margin: 0,
                        }}
                    >
                        Upload your resume and choose the role you're preparing for.
                    </p>
                </PixelWindow>

                <PixelWindow title="RESUME_UPLOAD" meta={file ? "1 file" : "0 files"}>
                    <ResumeUpload
                        file={file}
                        loading={loading && !candidateProfile}
                        candidateProfile={candidateProfile}
                        onSelect={handleResumeUpload}
                    />
                </PixelWindow>

                <PixelWindow title="TARGET_ROLE">
                    <RoleSelector value={targetRole} onChange={setTargetRole} />
                </PixelWindow>

                {error && <p className="error-text">{error}</p>}

                <button
                    className="btn-pixel btn-pixel--full"
                    onClick={handleStartInterview}
                    disabled={loading}
                >
                    {loading
                        ? "Preparing interview…"
                        : ready
                        ? "Start interview →"
                        : "Start interview"}
                </button>
            </div>
        </div>
    );
}

export default Setup;