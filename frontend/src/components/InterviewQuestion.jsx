const DIFFICULTY_CLASS = {
    easy: "badge--easy",
    medium: "badge--medium",
    hard: "badge--hard",
};

/**
 * InterviewQuestion
 * Props:
 *   question: { question: string, topic?: string, difficulty?: string }
 */
function InterviewQuestion({ question }) {
    const difficultyKey = (question.difficulty || "").toLowerCase();

    return (
        <div>
            <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
                {question.topic && (
                    <span className="badge badge--idle">{question.topic}</span>
                )}
                {question.difficulty && (
                    <span
                        className={`badge ${DIFFICULTY_CLASS[difficultyKey] || "badge--idle"}`}
                    >
                        {question.difficulty}
                    </span>
                )}
            </div>

            <p className="question-text">{question.question}</p>
        </div>
    );
}

export default InterviewQuestion;