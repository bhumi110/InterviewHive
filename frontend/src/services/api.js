import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
});

// RESUME

export async function parseResume(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await API.post("/resume/parse", formData);

        console.log("RESUME API RESPONSE:", response.data);

        return response.data;
    } catch (error) {
        console.error("Resume parsing error:", error.response?.data || error);
        throw error;
    }
}

// START INTERVIEW

export async function startInterview(candidateProfile, targetRole) {
    try {
        const response = await API.post("/interview/start", {
            candidate_profile: candidateProfile,
            target_role: targetRole,
        });

        console.log("START INTERVIEW RESPONSE:", response.data);

        return response.data;
    } catch (error) {
        console.error("Interview start error:", error.response?.data || error);
        throw error;
    }
}

// SUBMIT ANSWER

export async function submitAnswer(sessionId, answer) {
    const response = await API.post("/interview/answer", {
        session_id: sessionId,
        answer: answer,
    });

    return response.data;
}

// FINAL REPORT

export async function getReport(sessionId) {
    // NOTE: was `api.get` (lowercase, undefined) — fixed to use the
    // configured `API` axios instance so this actually works.
    const response = await API.get(`/report/${sessionId}`);

    return response.data;
}