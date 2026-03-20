from langchain_core.prompts import PromptTemplate

evaluation_prompt = """
You are an expert university examiner.

Evaluate ONLY the given question.

Question:
{question}

Correct Answer:
{context}

Student Answer:
{student_answer}

Instructions:
- Evaluate ONLY this question.
- Do NOT generate marks for other questions.
- Do NOT mention Q1–Q6 sections.

Output Format:

Marks: X/10

Reason:
Short explanation of why marks were given.

Missing Points:
- point 1
- point 2

Suggestion:
Short improvement suggestion.
"""