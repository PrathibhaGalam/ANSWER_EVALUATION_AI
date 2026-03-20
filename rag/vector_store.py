import chromadb
from chromadb.utils import embedding_functions


def create_vectorstore(chunks):

    client = chromadb.Client()

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="answer_scripts_ai",
        embedding_function=embedding_function
    )

    # Clear old data (important)
    try:
        collection.delete(where={})
    except:
        pass

    collection.add(
        documents=chunks,
        ids=[f"id_{i}" for i in range(len(chunks))]
    )

    return collection