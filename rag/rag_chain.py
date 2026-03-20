from config import llm
from prompts.evaluation_prompt import evaluation_prompt


def create_rag_chain(collection):

    def rag_chain(question, student_answer):

        # Retrieve relevant answers
        results = collection.query(
            query_texts=[question],
            n_results=3
        )

        docs = results["documents"][0]

        # Combine retrieved answers
        context = "\n".join(docs)

        # Create prompt
        prompt = evaluation_prompt.format(
            question=question,
            context=context,
            student_answer=student_answer
        )

        # LLM call
        response = llm.invoke(prompt)

        return response.content

    return rag_chain