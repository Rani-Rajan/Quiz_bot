from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    """
    Handles the main logic of the bot by processing user input and responding with questions or results.
    """
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id and current_question_id != 0:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the user's answer for the current question in the Django session.
    """
    if current_question_id is None:
        return True, ""  # No current question yet; this happens at the start.

    if not answer:
        return False, "Answer cannot be empty."

    user_answers = session.get("user_answers", {})
    user_answers[current_question_id] = answer
    session["user_answers"] = user_answers
    session.save()

    return True, ""


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    """
    if current_question_id is None:
        next_question_id = 0  # Start with the first question.
    else:
        next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]["question"]
        return next_question, next_question_id
    else:
        return None, None  # No more questions.


def generate_final_response(session):
    """
    Generates the final result message with the user's score.
    """
    user_answers = session.get("user_answers", {})
    score = 0

    for question_id, question_data in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question_data["answer"]
        user_answer = user_answers.get(question_id, "")
        if user_answer.strip().lower() == correct_answer.strip().lower():
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    return f"Quiz complete! You scored {score}/{total_questions}. Great job!" if total_questions > 0 else "No questions were attempted."
