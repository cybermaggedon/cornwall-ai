
from transformers import pipeline

# question_answerer = pipeline("question-answering", model="my_awesome_qa_model")

# question_answerer(question=question, context=context)
# {'score': 0.2058267742395401,
#  'start': 10,
#  'end': 95,
#  'answer': '176 billion parameters and can generate text in 46 languages natural languages and 13'}

class QuestionAnswerer:
    def __init__(self):

        # model_id = "distilbert-large-uncased"
        model_id = "distilbert-base-cased-distilled-squad"
        self.model = pipeline(
            "question-answering", model=model_id
        )

    def answer(self, question, context):
        ans = self.model(question=question, context=context)

        return ans["answer"], ans["score"], ans["start"], ans["end"]

