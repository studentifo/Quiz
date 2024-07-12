# Import necessary constants and data
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

# Function to record the user's answer for the current question
def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not current_question_id:
        return False, "No current question to answer."

    question = PYTHON_QUESTION_LIST[current_question_id]
    if answer not in question['options']:
        return False, f"Invalid answer. Please choose from {question['options']}."

    # Store the answer in the session
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][current_question_id] = answer

    return True, ""

# Function to get the next question based on the current question id
def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['text']
        return next_question, next_question_id
    else:
        return None, None

# Function to generate the final result message including the score
def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get('answers', {})
    score = 0

    for question_id, question in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question['correct_answer']
        user_answer = answers.get(question_id)
        if user_answer == correct_answer:
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    return f"You scored {score} out of {total_questions}."

# Function to generate bot responses based on user message and session state
def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
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
