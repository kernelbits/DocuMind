def build_prompt(user_query: str, context: str = None) -> list:
    system = (
        "You are a helpful assistant. IMPORTANT: Use ONLY the information provided in the PDF Context. "
        "Do NOT use outside knowledge or guess. If the answer is not present in the provided context, reply: "
        "'I cannot find an answer in the provided documents.' Be concise and conversational. "
        "When you use information from the context, include the source chunk numbers in parentheses, e.g. (Source: 1, 2)."
    )

    if context and context.strip():
        user = f"PDF Context:\n{context}\n\nQuestion: {user_query}\n\nAnswer strictly based on the PDF Context above."
    else:
        user = f"Question: {user_query}\n\nNote: No PDF context was found. If the answer is not in your documents, reply 'I cannot find an answer in the provided documents.'"

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]