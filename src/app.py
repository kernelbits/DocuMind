import asyncio
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
    await cl.Message("Upload a PDF to start").send()

@cl.on_message
async def main(message: cl.Message):
    files = [el for el in message.elements if hasattr(el, "path")]

    if files and not message.content:
        for file in files:
            try:
                processor = PDFProcessor()
                chunks, embeddings = await asyncio.to_thread(processor.process_pdf, file.path)
                await asyncio.to_thread(
                    collection.add,
                    embeddings=embeddings,
                    documents=chunks,
                    ids=[f"{file.name}_{uuid.uuid4()}" for _ in chunks],
                    metadatas=[{"source": file.name} for _ in chunks],
                )
            except Exception as e:
                await cl.Message(f"Failed to process {file.name}: {e}").send()
                return
        await cl.Message("PDF uploaded! Ask me a question about it.").send()
        return

    if not files and not message.content:
        await cl.Message("Please upload a PDF or ask a question.").send()
        return

    try:
        if files:
            for file in files:
                try:
                    processor = PDFProcessor()
                    chunks, embeddings = await asyncio.to_thread(processor.process_pdf, file.path)
                    await asyncio.to_thread(
                        collection.add,
                        embeddings=embeddings,
                        documents=chunks,
                        ids=[f"{file.name}_{uuid.uuid4()}" for _ in chunks],
                        metadatas=[{"source": file.name} for _ in chunks],
                    )
                except Exception as e:
                    await cl.Message(f"Failed to process {file.name}: {e}").send()
                    return

        relevant_content = await asyncio.to_thread(retrieve_context, message.content)

        prompt = build_prompt(message.content, relevant_content)

        try:
            prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in prompt])
            await asyncio.to_thread(save_log_chat, message.content, f"[PROMPT]\n{prompt_text}")
        except Exception:
            pass

        response = await asyncio.to_thread(ollama.chat, model="llama3.2:1b", messages=prompt)

        response_text = ""
        if isinstance(response, dict):
            response_text = response.get("message", {}).get("content") or ""
        else:
            response_text = str(response)

        await asyncio.to_thread(save_log_chat, message.content, response_text or "")

        await cl.Message(response_text or "No response from the model.").send()

    except Exception as e:
        await cl.Message(f"An error occurred: {e}").send()