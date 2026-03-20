from prompts.evaluation_prompt import evaluation_prompt
from config import llm
from rag.rag_chain import create_rag_chain
def evaluate_node(state):

    question = state.get("question")
    student_answer = state.get("student_answer")
    rag_chain = state.get("rag_chain")

    result = rag_chain(question, student_answer)

    return {
        "result": result
    }