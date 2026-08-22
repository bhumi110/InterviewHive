from app.agents.manager import manager_decision
from app.agents.interviewer import interviewer_agent
from app.agents.evaluator import evaluate_answer
from app.agents.skeptic import skeptic_agent


def run_interview_turn(
    state,
    blueprint,
    candidate_profile,
    candidate_answer=None
):

    evaluation = None
    signal = None
    skeptic_result = None

    # 1. EVALUATE PREVIOUS ANSWER

    if candidate_answer is not None:

        current_question = state.current_question

        evaluation = evaluate_answer(
            question=current_question,
            candidate_answer=candidate_answer,
            target_role=blueprint["target_role"]
        )

        # Store candidate answer
        state.conversation_history.append({
            "role": "candidate",
            "content": candidate_answer
        })

        state.answers.append(
            candidate_answer
        )

        # Convert evaluation into manager signal
        signal = {
            "overall_score": evaluation.overall_score,
            "technical_accuracy": evaluation.technical_accuracy,
            "depth": evaluation.depth,
            "reasoning": evaluation.reasoning,
            "should_challenge": evaluation.should_challenge,
            "state": determine_evaluation_state(
                evaluation
            )
        }

        state.evaluations.append(
            signal
        )

    # 2. SKEPTIC

    if candidate_answer is not None:

        skeptic_result = skeptic_agent(
            candidate_answer=candidate_answer,
            question=state.current_question,
            candidate_profile=candidate_profile
        )

    # 3. MANAGER DECIDES WHAT HAPPENS NEXT

    decision = manager_decision(
        state=state,
        blueprint=blueprint,
        evaluation=signal,
        skeptic_result=(
            skeptic_result.model_dump()
            if skeptic_result
            else None
        )
    )

    # 4. TERMINATE

    if decision["action"] == "finish":

        state.interview_status = "completed"

        return {
            "status": "completed",
            "decision": decision,
            "question": None,
            "interviewer_message": None,
            "evaluation": (
                evaluation.model_dump()
                if evaluation
                else None
            ),
            "skeptic": (
                skeptic_result.model_dump()
                if skeptic_result
                else None
            )
        }

    # 5. SKEPTIC CHALLENGE

    if decision["action"] == "challenge":

        challenge_question = (
            skeptic_result.challenge_question
        )

        state.current_question = {
            "question": challenge_question,
            "topic": decision["topic"],
            "difficulty": decision["difficulty"],
            "question_type": "challenge",
            "expected_concepts": []
        }

        state.questions_asked.append(
            challenge_question
        )

        state.question_count += 1

        state.conversation_history.append({
            "role": "interviewer",
            "content": challenge_question
        })

        return {
            "status": "in_progress",
            "decision": decision,
            "question": state.current_question,
            "interviewer_message": challenge_question,
            "evaluation": (
                evaluation.model_dump()
                if evaluation
                else None
            ),
            "skeptic": (
                skeptic_result.model_dump()
                if skeptic_result
                else None
            )
        }

    # 6. GENERATE NEXT QUESTION

    question = generate_unique_question(
        topic=decision["topic"],
        difficulty=decision["difficulty"],
        question_type="technical",
        previous_questions=state.questions_asked
    )

    # 7. INTERVIEWER AGENT

    interviewer_response = interviewer_agent(
        decision=decision,
        question=question.model_dump(),
        candidate_profile=candidate_profile,
        conversation_history=state.conversation_history,
        candidate_answer=candidate_answer
    )

    # 8. UPDATE STATE

    state.current_question = (
        question.model_dump()
    )

    state.current_topic = (
        question.topic
    )

    state.current_difficulty = (
        question.difficulty
    )

    state.questions_asked.append(
        question.question
    )

    state.conversation_history.append({
        "role": "interviewer",
        "content": interviewer_response.question
    })

    if question.topic not in state.topics_covered:

        state.topics_covered.append(
            question.topic
        )

    state.question_count += 1

    # 9. RETURN TURN

    return {
        "status": "in_progress",
        "decision": decision,
        "question": question.model_dump(),
        "interviewer_message": interviewer_response.question,
        "evaluation": (
            evaluation.model_dump()
            if evaluation
            else None
        ),
        "skeptic": (
            skeptic_result.model_dump()
            if skeptic_result
            else None
        )
    }