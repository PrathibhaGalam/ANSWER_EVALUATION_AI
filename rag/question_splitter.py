import re


def split_questions(text):

    questions = {}

    pattern = r"(Q[1-6])[:\-\s]*(.*?)(?=Q[1-6]|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    for q, ans in matches:
        questions[q.strip()] = ans.strip()

    return questions


def split_student_answers(text):

    answers = {}

    pattern = r"(Q[1-6])[:\-\s]*(.*?)(?=Q[1-6]|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    for q, ans in matches:
        answers[q.strip()] = ans.strip()

    return answers