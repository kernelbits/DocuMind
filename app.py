import chainlit as cl
from src.rag import query_rag
@cl.on_chat_start
async def start():
    """
    This runs when the user opens the page.
    We send a welcome message.
    """
    await cl.Message(content="👋 Welcome to DocuMind! I am ready to answer questions about your documents.").send()

@cl.on_message
async def main(message: cl.Message):
    """
    This runs every time the user types a message.
    """
    user_query = message.content

    # 1. Show a "Processing" status
    msg = cl.Message(content="")
    await msg.send()
    
    # 2. Call your Logic
    # Note: query_rag is synchronous (blocking), so we run it directly.
    # In a huge app, we would make this async, but for i3 laptop, this is fine.
    answer, source_documents = query_rag(user_query)

    # 3. Format Sources (Citations)
    # We create nice little text boxes for the sources
    source_elements = []
    for i, doc in enumerate(source_documents):
        source_name = f"Source {i+1}"
        # Create a text element for the UI
        element = cl.Text(name=source_name, content=doc.page_content, display="inline")
        source_elements.append(element)

    # 4. Send the Final Answer
    msg.content = answer
    msg.elements = source_elements
    await msg.update()