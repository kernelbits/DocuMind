import ollama
import chainlit as cl 
from processor import PDFProcessor
from database import collection
from chat_logger import save_log_chat
from retriever import retrieve_context
from prompt_builder import build_prompt
import uuid


@cl.on_chat_start
async def start():
    await cl.Message("Upload a pdf to start").send()



@cl.on_message
async def main(message: cl.Message):
    if not message.content:
        await cl.Message("Pdf uploaded ask anything ! ").send()
        return 
    files = [element for element in message.elements if hasattr(element,"path")]
    if files:
        for file in files:
            processor = PDFProcessor()
            chunks,embeddings = processor.process_pdf(file.path)
            collection.add(
                embeddings=embeddings,
                documents=chunks,
                ids= [f"{file.name}_{uuid.uuid4()}" for _ in chunks],
                metadatas=[{"source": file.name} for _ in chunks]
            )
    relevant_content = retrieve_context(message.content)
    prompt = build_prompt(message.content,relevant_content)
    response = ollama.chat(
        model="llama3.2:1b",
        messages=prompt
    )
    
    save_log_chat(message.content,response['message']['content'])

    await cl.Message(response["message"]['content']).send()


    