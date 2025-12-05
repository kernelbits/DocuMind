from ollama import chat
import chainlit as cl 
from processor import PDFProcessor
from database import collection

@cl.on_chat_start
async def start():
    await cl.Message("Upload a pdf to start").send()

@cl.on_message
async def main(message: cl.Message):
    stream = chat(
    model='llama3.2:1b',
    messages=[{'role': 'user', 'content': message.content}],
    stream=True,
)   
    response = ""
    for chunk in stream:
        response += chunk['message']['content']
    
    await cl.Message(
    content=response
  ).send()


@cl.on_message
async def main(message: cl.Message):
    files = [element for element in message.elements if hasattr(element,"path")]
    if files:
        for file in files:
            processor = PDFProcessor()
            chunks,embeddings = processor.process_pdf(file.path)
            collection.add(
                embeddings=embeddings,
                chunks=chunks,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )

    query_emb = processor.embed_query(message.content)
    result = collection.query(
        query_embeddings=query_emb,
        n_results=4
    )
    