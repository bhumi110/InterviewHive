def should_end_interview(state):

    if state.question_count >= state.max_questions:
        return True

    if state.time_remaining <= 0:
        return True

    return False


def should_follow_up(evaluation):

    if evaluation["should_challenge"]:
        return True

    if evaluation["state"] in [
        "shallow",
        "weak_reasoning"
    ]:
        return True

    return False


def choose_next_topic(
    state,
    blueprint
):

    priority_topics = blueprint[
        "priority_topics"
    ]

    for topic in priority_topics:

        if topic not in state.topics_covered:
            return topic

    for topic in priority_topics:
        return topic

    return "General"


def determine_answer_state(evaluation):

    if evaluation["technical_accuracy"] < 5:
        return "technical_gap"

    if evaluation["depth"] < 5:
        return "shallow"

    if evaluation["reasoning"] < 5:
        return "weak_reasoning"

    if evaluation["overall_score"] >= 8:
        return "strong"

    return "acceptable"


MAX_FOLLOW_UPS = 2


def can_follow_up(state):

    return (
        state.follow_up_count
        < MAX_FOLLOW_UPS
    )


DIFFICULTY_LEVELS = [
    "easy",
    "medium",
    "hard"
]


def adjust_difficulty(
    current_difficulty,
    answer_state
):

    current_index = DIFFICULTY_LEVELS.index(
        current_difficulty
    )

    if answer_state == "strong":

        new_index = min(
            current_index + 1,
            len(DIFFICULTY_LEVELS) - 1
        )

    elif answer_state in [
        "technical_gap",
        "shallow"
    ]:

        new_index = max(
            current_index - 1,
            0
        )

    else:

        new_index = current_index

    return DIFFICULTY_LEVELS[new_index]