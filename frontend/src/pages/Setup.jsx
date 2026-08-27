import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    parseResume,
    startInterview
} from "../services/api";


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

            setCandidateProfile(
                data.candidate_profile || data
            );

        } catch (err) {

            console.error(err);

            setError(
                "Could not analyse your resume."
            );

            setCandidateProfile(null);

        } finally {

            setLoading(false);

        }
    }


    async function handleStartInterview() {

        if (!candidateProfile) {

            setError(
                "Please upload your resume first."
            );

            return;
        }

        if (!targetRole.trim()) {

            setError(
                "Please enter your target role."
            );

            return;
        }

        setError("");
        setLoading(true);

        try {

            const data = await startInterview(
                candidateProfile,
                targetRole
            );

            /*
             * Store session information temporarily.
             * No login or permanent user storage.
             */

            sessionStorage.setItem(
                "interview_session",
                JSON.stringify({
                    sessionId: data.session_id,
                    candidateProfile,
                    targetRole
                })
            );

            navigate("/interview");

        } catch (err) {

    console.error(
        "Resume upload failed:",
        err
    );

    const message =
        err.response?.data?.detail ||
        "Could not analyse your resume.";

    setError(message);

    setCandidateProfile(null);
}
    }


    return (

        <main>

            <h1>
                Set up your interview
            </h1>

            <p>
                Upload your resume and choose
                the role you're preparing for.
            </p>


            {/* Resume */}

            <section>

                <h2>
                    Your resume
                </h2>

                <input
                    type="file"
                    accept=".pdf"
                    onChange={(event) =>
                        handleResumeUpload(
                            event.target.files[0]
                        )
                    }
                />

                {file && (
                    <p>
                        {file.name}
                    </p>
                )}

                {loading && (
                    <p>
                        Analysing...
                    </p>
                )}

                {candidateProfile && !loading && (
                    <p>
                        ✓ Resume analysed
                    </p>
                )}

            </section>


            {/* Target role */}

            <section>

                <h2>
                    Target role
                </h2>

                <input
                    type="text"
                    placeholder="e.g. Data Scientist"
                    value={targetRole}
                    onChange={(event) =>
                        setTargetRole(
                            event.target.value
                        )
                    }
                />

            </section>


            {/* Error */}

            {error && (
                <p>
                    {error}
                </p>
            )}


            {/* Start */}

            <button
                onClick={handleStartInterview}
                disabled={loading}
            >
                {loading
                    ? "Preparing interview..."
                    : "Start Interview"
                }
            </button>

        </main>

    );
}


export default Setup;