
"""
Defines class Embedding which takes an English-language sentence
and returns an embeddeding.  The model used here uses the
sentence-transformers/all-MiniLM-L6-v2 model from Hugging Face which maps
sentences and paragraphs to a 384 dimensional dense vector space.

Usage:
    e = Embedding()
    emb = e.get("How are you today?")

See https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
"""

from sentence_transformers import SentenceTransformer

class Embedding:
    """
    Maps sentences to a 384-dim vector using
    sentence-transformers/all-MiniLM-L6-v2
    """

    def __init__(self):
        """
        Initialises, loads the model may occur a multi-second load time,
        and possible a large network download on first use
        """

        self.model_id = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = None

    def get(self, text):
        "Maps English text to a 384-vector embedding"

        if self.model == None:
            self.model = SentenceTransformer(self.model_id)

        return self.model.encode(text)

    
