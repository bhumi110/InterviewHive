import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { submitAnswer } from "../services/api";

function Interview() {

    const location = useLocation();
    const navigate = useNavigate();

    const sessionId = location.state?.sessionId;
    const initialQuestion = location.state?.question;
    const initialMessage = location.state?.interviewerMessage;

    const [question, setQuestion] = useState(
        initialQuestion || null
    );

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
            <div>
                <h1>
                    No active interview
                </h1>

                <button
                    onClick={() => navigate("/setup")}
                >
                    Go to Setup
                </button>
            </div>
        );
    }


    async function handleSubmit() {

        if (!answer.trim()) {
            return;
        }

        setLoading(true);
        setError("");

        try {

            const result = await submitAnswer(
                sessionId,
                answer
            );

            console.log(
                "INTERVIEW TURN:",
                result
            );


            // Interview finished
            if (result.status === "completed") {

                navigate(
                    "/report",
                    {
                        state: {
                            sessionId: sessionId
                        }
                    }
                );

                return;
            }


            // Update next question
            setQuestion(
                result.question
            );


            // Update interviewer dialogue
            setInterviewerMessage(
                result.interviewer_message || ""
            );


            // Clear answer box
            setAnswer("");


            // Increment question number
            setQuestionNumber(
                previous => previous + 1
            );

        } catch (err) {

            console.error(
                "Answer submission error:",
                err
            );

            setError(
                "Something went wrong while processing your answer."
            );

        } finally {

            setLoading(false);
        }
    }


    return (

        <div
            style={{
                minHeight: "100vh",
                padding: "40px",
                fontFamily: "Arial, sans-serif"
            }}
        >

            {/* Header */}

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "40px"
                }}
            >

                <h1>
                    InterviewHive
                </h1>

                <span>
                    Question {questionNumber}
                </span>

            </div>


            {/* Interviewer */}

            <div
                style={{
                    marginBottom: "30px"
                }}
            >

                <h2>
                    AI Interviewer
                </h2>

                <p>
                    {interviewerMessage ||
                        "Let's begin the interview."}
                </p>

            </div>


            {/* Question */}

            <div
                style={{
                    marginBottom: "30px"
                }}
            >

                <h2>
                    {question.question}
                </h2>

                <p>
                    Topic: {question.topic}
                </p>

                <p>
                    Difficulty: {question.difficulty}
                </p>

            </div>


            {/* Answer */}

            <div>

                <textarea
                    value={answer}
                    onChange={(event) =>
                        setAnswer(event.target.value)
                    }
                    placeholder="Type your answer here..."
                    rows={8}
                    disabled={loading}
                    style={{
                        width: "100%",
                        maxWidth: "800px",
                        padding: "15px",
                        fontSize: "16px",
                        resize: "vertical"
                    }}
                />

            </div>


            {/* Error */}

            {error && (

                <p>
                    {error}
                </p>

            )}


            {/* Submit */}

            <button
                onClick={handleSubmit}
                disabled={
                    loading ||
                    !answer.trim()
                }
                style={{
                    marginTop: "20px",
                    padding: "12px 24px",
                    cursor: "pointer"
                }}
            >

                {loading
                    ? "Evaluating..."
                    : "Submit Answer"}

            </button>

        </div>
    );
}


export default Interview;