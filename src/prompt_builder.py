def build_prompt(user_query: str, context: str = None) -> list:
    sys_prompt = "You are a helpful assistant. Use provided context if relevant, otherwise answer from your knowledge."
    
    if context and context.strip(): 
        user_prompt = f"""PDF Context:
{context}

---

User Question: {user_query}"""
    else:
        user_prompt = f"User Question: {user_query}"
    
    return [
        {'role': 'system', 'content': sys_prompt},
        {'role': 'user', 'content': user_prompt}
    ]