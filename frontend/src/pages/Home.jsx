import { useNavigate } from "react-router-dom";

import PixelWindow from "../pixi/pixelWindow";
import InterviewRoomScene from "../pixi/Interviewroomscene";
import AgentRoster from "../pixi/agentRoster";
import logo from "../assets/logo.png";

function Home() {
    const navigate = useNavigate();

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
                <span className="app-topbar__meta">v0.1.0 · practice mode</span>
            </div>

            <div className="app-shell__inner">
                {/* <PixelWindow title="AI_INTERVIEW_ROOM" meta="idle" tight>
                    <InterviewRoomScene phase="idle" height={160} />
                </PixelWindow> */}

                <PixelWindow title="AI_INTERVIEW_ROOM" meta="4 agents">
                    <div className="eyebrow">meet your panel</div>
                    <AgentRoster phase="idle" />
                </PixelWindow>

                <PixelWindow title="README.txt">
                    <div className="eyebrow">welcome</div>

                    <h1 style={{ fontSize: 20, marginBottom: 14 }}>
                        AI Interview Room
                    </h1>

                    <p
                        style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: 14,
                            lineHeight: 1.6,
                            color: "var(--ink-dim)",
                            maxWidth: 520,
                            marginBottom: 22,
                        }}
                    >
                        Practice realistic technical interviews tailored to your
                        resume. Upload your resume, pick a target role, and the
                        interviewer will ask questions built around your actual
                        experience — then score your performance at the end.
                    </p>

                    <button
                        className="btn-pixel"
                        onClick={() => navigate("/setup")}
                    >
                        Start interview →
                    </button>
                </PixelWindow>

                
            </div>
        </div>
    );
}

export default Home;