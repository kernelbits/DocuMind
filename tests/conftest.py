import sys
import types

# src/reader.py imports sentence_transformers at module level, which pulls in
# torch and downloads models on first use. The tests only exercise the text
# chunker, which never touches the embedding model, so replace the module with
# a stub. Nothing in the test suite loads a real model.
if "sentence_transformers" not in sys.modules:
    _stub = types.ModuleType("sentence_transformers")

    class SentenceTransformer:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Embedding models are not loaded in the test suite")

    _stub.SentenceTransformer = SentenceTransformer
    sys.modules["sentence_transformers"] = _stub
