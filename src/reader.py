# Pdf Reading and Storing in Database 

from pypdf import PdfReader


def read_pdf(path):
    try:
        reader = PdfReader(path)
        page_text = [page.extract_text() for page in reader.pages if page.extract_text()]
        text = '\n\n'.join(page_text)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        print(f"Error type: {type(e).__name__}")
        return ""
    
    return text


def chunk_text(text: str,chunk_size=600,overlap=50):
    if not isinstance(text,str):
        raise ValueError("Text must be a string ")
    if not isinstance(chunk_size,int) and isinstance(overlap,int):
        raise ValueError("chunk_size and overlap must be integers ")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap 
    return chunks 


pdf = read_pdf("./data/norse.pdf")
print(pdf[100:])
chunks = chunk_text(pdf)
print(len(chunks))