
"""
Defines a TextQuery class which answers questions based on textual body
of work.  Works well in small-to-medium-sized bodies of text e.g. blog
posts and wikipedia pages.

Distil* is a class of compressed models that started with DistilBERT.
DistilBERT stands for Distilled-BERT. DistilBERT is a small, fast, cheap
and light Transformer model based on Bert architecture. It has 40% less
parameters than bert-base-uncased, runs 60% faster while preserving 97% of
BERT's performances as measured on the GLUE language understanding
benchmark.

Usage:

    # Create query model
    tq = TextQuery()

    # Execute query
    ans = tq.query("What is the largest city in the world?")

    # The results have a show method
    for an in ans:
        ans.show()

See: https://huggingface.co/distilbert-base-cased-distilled-squad

Model proposed at:
https://medium.com/huggingface/distilbert-8cf3380435b5
"""

from transformers import pipeline
from result import *

class TextQuery:
    """
    Returns results from querying a body of text using an English language
    query using the distilbert-base-cased-distilled-squad model.
    May occur a multi-second load time, and possible a large network download
    on first use.  These models are 100s of MB.
    """

    # Model ID
    model_id = "distilbert-base-cased-distilled-squad"

    # Pipeline.  Pipeline stores no state, so can be shared by multiple
    # class instances.
    model = None

    @staticmethod
    def create(text):
        "Initialise the model with a body of text to query"
        return TextQuery(text)

    def __init__(self, text):
        "Initialise the model with a body of text to query"
        self.text = text

    def query(self, question):
        "Query the model, returning a Result array"

        if TextQuery.model == None:
            TextQuery.model = pipeline(
                "question-answering", model=TextQuery.model_id
            )

        ans = TextQuery.model(question=question, context=self.text)

        return [TextResult(ans["answer"])]

