from app.services.interview_logic import (
    should_end_interview,
    choose_next_topic,
    determine_answer_state,
    should_follow_up,
    can_follow_up,
    adjust_difficulty,
)


def manager_decision(
    state,
    blueprint,
    evaluation=None,
    skeptic_result=None
):

    if should_end_interview(state):

        state.interview_status = "completed"

        return {
            "action": "finish",
            "reason": "Interview limit reached"
        }

    # Interview hasn't started
    if state.interview_status == "not_started":

        state.interview_status = "in_progress"

        topic = choose_next_topic(
            state,
            blueprint
        )

        return {
            "action": "ask_question",
            "topic": topic,
            "difficulty": state.current_difficulty,
            "reason": "Start interview"
        }

    # We have an evaluation
    if evaluation is not None:

        answer_state = determine_answer_state(
            evaluation
        )

        # Follow-up
        if (
            should_follow_up(evaluation)
            and can_follow_up(state)
        ):

            state.follow_up_count += 1

            return {
                "action": "follow_up",
                "topic": state.current_topic,
                "difficulty": state.current_difficulty,
                "reason": answer_state
            }

        # Reset follow-up counter
        state.follow_up_count = 0

        # Adapt difficulty
        state.current_difficulty = adjust_difficulty(
            state.current_difficulty,
            answer_state
        )

        # Choose new topic
        topic = choose_next_topic(
            state,
            blueprint
        )

        return {
            "action": "ask_question",
            "topic": topic,
            "difficulty": state.current_difficulty,
            "reason": answer_state
        }

    return {
        "action": "ask_question",
        "topic": choose_next_topic(
            state,
            blueprint
        ),
        "difficulty": state.current_difficulty,
        "reason": "Default"
    }