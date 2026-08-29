import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getReport } from "../services/api";


function Report() {

    const navigate = useNavigate();

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        async function loadReport() {

            try {

                const storedSession =
                    sessionStorage.getItem(
                        "interview_session"
                    );

                if (!storedSession) {

                    setError(
                        "No interview session found."
                    );

                    setLoading(false);

                    return;
                }


                const session =
                    JSON.parse(storedSession);


                const data = await getReport(
                    session.sessionId
                );


                setReport(
                    data.report
                );

            } catch (err) {

                console.error(
                    "Report loading error:",
                    err
                );

                setError(
                    err.response?.data?.detail ||
                    "Could not load interview report."
                );

            } finally {

                setLoading(false);
            }
        }


        loadReport();

    }, []);


    if (loading) {

        return (
            <div>
                <h1>
                    Generating your report...
                </h1>

                <p>
                    Evaluating your complete interview.
                </p>
            </div>
        );
    }


    if (error) {

        return (
            <div>

                <h1>
                    Could not load report
                </h1>

                <p>
                    {error}
                </p>

                <button
                    onClick={() =>
                        navigate("/setup")
                    }
                >
                    Start New Interview
                </button>

            </div>
        );
    }


    if (!report) {
        return null;
    }


    return (

        <main>

            <h1>
                Interview Report
            </h1>


            {/* Overall */}

            <section>

                <h2>
                    Overall Score
                </h2>

                <div>
                    {report.overall_score}/10
                </div>

            </section>


            {/* Scores */}

            <section>

                <h2>
                    Performance
                </h2>

                <p>
                    Technical:
                    {" "}
                    {report.technical_score}/10
                </p>

                <p>
                    Problem Solving:
                    {" "}
                    {report.problem_solving_score}/10
                </p>

                <p>
                    Communication:
                    {" "}
                    {report.communication_score}/10
                </p>

                <p>
                    Confidence:
                    {" "}
                    {report.confidence_score}/10
                </p>

                <p>
                    Technical Depth:
                    {" "}
                    {report.depth_score}/10
                </p>

            </section>


            {/* Strengths */}

            <section>

                <h2>
                    Strengths
                </h2>

                {report.strengths.map(
                    (strength, index) => (

                        <p key={index}>
                            ✓ {strength}
                        </p>

                    )
                )}

            </section>


            {/* Weaknesses */}

            <section>

                <h2>
                    Areas to Improve
                </h2>

                {report.weaknesses.map(
                    (weakness, index) => (

                        <p key={index}>
                            • {weakness}
                        </p>

                    )
                )}

            </section>


            {/* Red flags */}

            {report.red_flags.length > 0 && (

                <section>

                    <h2>
                        Red Flags
                    </h2>

                    {report.red_flags.map(
                        (flag, index) => (

                            <p key={index}>
                                ⚠ {flag}
                            </p>

                        )
                    )}

                </section>

            )}


            {/* Recommended topics */}

            <section>

                <h2>
                    Recommended Topics
                </h2>

                {report.recommended_topics.map(
                    (topic, index) => (

                        <p key={index}>
                            {index + 1}. {topic}
                        </p>

                    )
                )}

            </section>


            {/* Summary */}

            <section>

                <h2>
                    Interview Summary
                </h2>

                <p>
                    {report.summary}
                </p>

            </section>


            <button
                onClick={() =>
                    navigate("/setup")
                }
            >
                Practice Again
            </button>

        </main>
    );
}


export default Report;