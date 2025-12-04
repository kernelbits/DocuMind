from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


DB_PATH = "db/"
LLM_MODEL = "llama3.2:1b" 

PROMPT_TEMPLATE = """
You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If the answer is not in the context, say "I do not know" and do not make up facts.

Context:
{context}

Question: {question}
"""
def query_rag(query_text):
    """
    1. Load DB
    2. Search for relevant text
    3. Send to LLM
    """

    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    results = db.similarity_search(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    final_prompt = prompt_template.format(context=context_text, question=query_text)
    print(" AI is thinking...")
    model = ChatOllama(model=LLM_MODEL)
    response = model.invoke(final_prompt)
    return response.content, results
