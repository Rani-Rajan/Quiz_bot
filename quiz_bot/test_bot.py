# test_bot.py
from quiz_bot import generate_bot_responses  # Replace with actual import path

class MockSession(dict):
    def save(self):
        pass

session = MockSession()
user_inputs = ["def", "14", "append"]  # User's answers for the quiz
bot_responses = []

for user_input in user_inputs:
    bot_responses.extend(generate_bot_responses(user_input, session))

# Handle the final message after all questions are answered
bot_responses.extend(generate_bot_responses("", session))  # Empty input to trigger final response

for response in bot_responses:
    print(response)
