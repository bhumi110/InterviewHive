import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { submitAnswer } from "../services/api";

import PixelWindow from "../pixi/pixelWindow";
import InterviewRoomScene from "../pixi/Interviewroomscene";
import InterviewHeader from "../components/InterviewHeader";
import InterviewQuestion from "../components/InterviewQuestion";
import AnswerInput from "../components/AnswerInput";
import AgentRoster from "../pixi/agentRoster";
import logo from "../assets/logo.png";


function Interview() {
    const location = useLocation();
    const navigate = useNavigate();

    const storedInterview = JSON.parse(
        sessionStorage.getItem("interview_session") || "null"
    );

    const sessionId = location.state?.sessionId || storedInterview?.sessionId;

    const initialQuestion =
        location.state?.question || storedInterview?.question;

    const initialMessage =
        location.state?.interviewerMessage || storedInterview?.interviewerMessage;

    const [question, setQuestion] = useState(initialQuestion || null);

    const [interviewerMessage, setInterviewerMessage] = useState(
        initialMessage || ""
    );

    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [questionNumber, setQuestionNumber] = useState(1);

    // If user opens /interview directly
    if (!sessionId || !question) {
        return (
            <div className="app-shell">
                <div className="app-shell__inner">
                    <PixelWindow title="ERROR">
                        <h1 style={{ fontSize: 16, marginBottom: 14 }}>
                            No active interview
                        </h1>
                        <button
                            className="btn-pixel"
                            onClick={() => navigate("/setup")}
                        >
                            Go to setup →
                        </button>
                    </PixelWindow>
                </div>
            </div>
        );
    }

    async function handleSubmit() {
        if (!answer.trim()) return;

        setLoading(true);
        setError("");

        try {
            const result = await submitAnswer(sessionId, answer);

            console.log("INTERVIEW TURN:", result);

            // Interview finished
            if (result.status === "completed") {
                navigate("/report");
                return;
            }

            // Update next question
            setQuestion(result.question);

            // Update interviewer dialogue
            setInterviewerMessage(result.interviewer_message || "");

            sessionStorage.setItem(
                "interview_session",
                JSON.stringify({
                    ...JSON.parse(
                        sessionStorage.getItem("interview_session") || "{}"
                    ),
                    question: result.question,
                    interviewerMessage: result.interviewer_message,
                })
            );

            // Clear answer box
            setAnswer("");

            // Increment question number
            setQuestionNumber((previous) => previous + 1);
        } catch (err) {
            console.error("Answer submission error:", err);
            setError("Something went wrong while processing your answer.");
        } finally {
            setLoading(false);
        }
    }

    const phase = loading ? "thinking" : answer.trim() ? "listening" : "idle";

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
                <span className="app-topbar__meta">live session</span>
            </div>

            <div className="app-shell__inner">
                <section className="pw">
                    <InterviewHeader
                        questionNumber={questionNumber}
                        phase={phase}
                    />
                    <InterviewRoomScene phase={phase} height={150} />
                </section>

                <PixelWindow
                    title="AGENT_PANEL"
                    meta={phase === "thinking" ? "deliberating…" : "4 agents"}
                >
                    <AgentRoster phase={phase} />
                </PixelWindow>

                {interviewerMessage && (
                    <div className="terminal-block">
                        <div className="terminal-line">
                            <span className="prompt">interviewer&gt;</span>
                            <span>{interviewerMessage}</span>
                        </div>
                    </div>
                )}

                <PixelWindow title="QUESTION">
                    <InterviewQuestion question={question} />
                </PixelWindow>

                <PixelWindow title="ANSWER">
                    <AnswerInput
                        value={answer}
                        onChange={setAnswer}
                        onSubmit={handleSubmit}
                        loading={loading}
                    />

                    {error && (
                        <p className="error-text" style={{ marginTop: 12 }}>
                            {error}
                        </p>
                    )}
                </PixelWindow>
            </div>
        </div>
    );
}

export default Interview;