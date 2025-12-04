import sys
import time
import argparse
from src.rag import query_rag

# ANSI Color codes for a pretty terminal
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_answer(answer, sources, duration):
    """
    Formats the AI response and sources for the terminal
    """
    print("\n" + "="*60)
    print(f"{CYAN}🤖 AI Answer:{RESET}")
    print(answer)
    print("="*60)
    
    print(f"\n{YELLOW}📚 Sources Used:{RESET}")
    if not sources:
        print("No specific sources cited.")
    else:
        for i, doc in enumerate(sources):
            # Try to get metadata, fallback to defaults if missing
            source_name = doc.metadata.get('source', 'Unknown File')
            page_num = doc.metadata.get('page', 'N/A')
            
            print(f"   {i+1}. {source_name} (Page {page_num})")
            # Optional: Print a tiny snippet of the text
            # snippet = doc.page_content.replace('\n', ' ')[:100]
            # print(f"      \"{snippet}...\"")

    print(f"\n⏱️  Time taken: {duration:.2f}s")
    print("-" * 60 + "\n")

def main():
    # Setup Argument Parser
    parser = argparse.ArgumentParser(description="DocuMind CLI - Chat with your PDFs")
    parser.add_argument("query", nargs="?", type=str, help="The question to ask (optional)")
    args = parser.parse_args()

    # Mode 1: One-shot Query (e.g., python main.py "Summary")
    if args.query:
        start_time = time.time()
        answer, sources = query_rag(args.query)
        end_time = time.time()
        print_answer(answer, sources, end_time - start_time)
        return

    # Mode 2: Interactive Chat Loop
    print(f"{GREEN}=== DocuMind CLI (Interactive Mode) ==={RESET}")
    print("Type 'exit', 'quit', or 'q' to stop.")

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nExiting...")
            break

        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Bye!")
            break

        start_time = time.time()
        
        # Call the Brain
        # IMPORTANT: Now receiving two values (Answer + Documents)
        answer, sources = query_rag(user_input)
        
        end_time = time.time()
        
        print_answer(answer, sources, end_time - start_time)

if __name__ == "__main__":
    main()