from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def generate_embedding(text):
    """
    Generates a vector embedding for the given text using the preloaded model.
    """
    return embeddings.embed_query(text)