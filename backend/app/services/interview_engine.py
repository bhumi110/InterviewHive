from app.services.interview_logic import (
    should_end_interview,
    generate_unique_question
)

from app.agents.manager import manager_decision
from app.agents.interviewer import interviewer_agent
from app.agents.evaluator import evaluate_answer
from app.agents.skeptic import skeptic_agent
from app.agents.judge import judge_agent


def run_interview_turn(
    state,
    blueprint,
    candidate_profile,
    candidate_answer=None
):

    evaluation = None
    skeptic_result = None

    # EVALUATE PREVIOUS ANSWER

    if candidate_answer is not None:

        current_question = state.current_question

        evaluation = evaluate_answer(
        current_question,
        candidate_answer,
        state.target_role
    )

        state.conversation_history.append({
            "role": "candidate",
            "content": candidate_answer
        })

        state.answers.append(
            candidate_answer
        )

        state.evaluations.append(
            evaluation.model_dump()
        )

    # SKEPTIC

    if candidate_answer is not None:

        skeptic_result = skeptic_agent(
            candidate_answer=candidate_answer,
            question=state.current_question,
            candidate_profile=candidate_profile
        )

    # MANAGER

    decision = manager_decision(
        state=state,
        blueprint=blueprint,
        evaluation=(
            evaluation.model_dump()
            if evaluation
            else None
        ),
        skeptic_result=(
            skeptic_result.model_dump()
            if skeptic_result
            else None
        )
    )

    #TERMINATE?

    if decision["action"] == "finish":

        state.interview_status = "completed"

        return {
            "status": "completed",
            "decision": decision,
            "question": None,
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

    #SKEPTIC CHALLENGE

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

    #GENERATE NEW QUESTION

    question = generate_unique_question(
        topic=decision["topic"],
        difficulty=decision["difficulty"],
        question_type="technical",
        previous_questions=state.questions_asked
    )

    #INTERVIEWER

    interviewer_response = interviewer_agent(
        decision=decision,
        question=question.model_dump(),
        candidate_profile=candidate_profile,
        conversation_history=state.conversation_history,
        candidate_answer=candidate_answer
    )

    #UPDATE STATE

    state.current_question = (
        question.model_dump()
    )

    state.current_topic = (
        question.topic
    )

    state.current_difficulty = (
        question.difficulty
    )

    state.conversation_history.append({
        "role": "interviewer",
        "content": interviewer_response.question
    })

    state.questions_asked.append(
        question.question
    )

    if question.topic not in state.topics_covered:

        state.topics_covered.append(
            question.topic
        )

    state.question_count += 1

    #RETURN

    return {
        "status": "in_progress",

        "decision": decision,

        "question": question.model_dump(),

        "interviewer_message": (
            interviewer_response.question
        ),

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
    
def generate_final_report(
        state,
        candidate_profile,
        target_role
    ):

        report = judge_agent(
            candidate_profile=candidate_profile,
            target_role=target_role,
            questions=state.questions_asked,
            answers=state.answers,
            evaluations=state.evaluations,
            topics_covered=state.topics_covered
        )

        state.final_report = report.model_dump()

        return report