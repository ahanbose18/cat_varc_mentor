import re
import requests
import logging
from openai import OpenAI , OpenAIError, RateLimitError, AuthenticationError



def evaluate_user_answers(generated_output, user_answers):
    correct_answers = re.findall(r'Answer:\s*([A-D])', generated_output)
    evaluation = []
    for i, (correct, user) in enumerate(zip(correct_answers, user_answers)):
        result = 'Correct' if correct.upper() == user.upper() else f'Wrong (Correct: {correct})'
        evaluation.append(f"Q{i+1}: {result}")
    return evaluation
