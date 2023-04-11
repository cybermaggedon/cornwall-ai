
"""
Defines class TableQuery which implements the TAPAS large model which can
query tables in response to English-language questions.  Queries result
in an array of Results.

Example:

    # Fetch data as Pandas dataframe
    table = pd.read_csv("my-data-file.csv")

    # Create table query model
    tq = TableQuery(table)

    # Execute query
    ans = tq.query("What is the world's tallest build?")

    # The results have a show method
    for an in ans:
        ans.show()

See https://huggingface.co/google/tapas-large-finetuned-wtq

TAPAS model was proposed at:
https://www.aclweb.org/anthology/2020.acl-main.398
https://www.aclweb.org/anthology/2020.findings-emnlp.27/
"""

from transformers import TapasTokenizer, TapasForQuestionAnswering
import pandas as pd
from result import *

class TableQuery:
    """
    Returns results from querying a table using an English language query
    using the google/tapas-large-finetuned-wtq model from Hugging Face.
    """

    @staticmethod
    def create(table):
        """
        Initialise the model from a dataframe provided.  To be useful,
        the dataframe should have column headers labelled using English
        language column headers.  May occur a multi-second load time,
        and possible a large network download on first use.  These models
        are 100s of MB.  table = a Pandas dataframe of the CSV.
        """
        return TableQuery(table)

    def __init__(self, table):
        """
        Initialise the model from a dataframe provided.  To be useful,
        the dataframe should have column headers labelled using English
        language column headers.  May occur a multi-second load time,
        and possible a large network download on first use.  These models
        are 100s of MB.  table = a Pandas dataframe of the CSV.
        """

        # Table cells must be strings, this does a conversion
        self.table = table.astype(str)

        # Initialise on demand
        self.model = None

    def init_model(self):

        # The model pathnames on Hugging Face.  Tokeniser and model path
        # TAPAS fine-tune trained on WikiTable questions
        self.tk_path = "google/tapas-large-finetuned-wtq"
        self.model_path = "google/tapas-large-finetuned-wtq"

        # Load pretrained tokenizer
        self.tokenizer = TapasTokenizer.from_pretrained(self.tk_path)

        # Load pretrained model
        self.model = TapasForQuestionAnswering.from_pretrained(self.model_path)

    def query(self, query):
        """
        Query the table using an English-language question, returning a
        Result array.
        """

        if self.model == None:
            self.init_model()

        # Tokenise the question to tensors
        inputs = self.tokenizer(
            table=self.table, queries=[query], padding='max_length',
            truncation=True, return_tensors="pt"
        )

        # Generate model results from tensors
        outputs = self.model(**inputs)

        # Convert logits to table cell coordinates
        coords, operators = self.tokenizer.convert_logits_to_predictions(
            inputs, outputs.logits.detach(), outputs.logits_aggregation.detach()
        )

        # Internal post-processing to get answers and cells
        aggreg, answers, cells = self.postprocess_predictions(
            operators, coords
        )

        # Return answers and cell results
        return [
            TextResult(answers[0]),
            TableResult(self.table, cells[0])
        ]

    def postprocess_predictions(self, operators, coords):
        """
        Compute the predicted operation and nicely structure the answers.
        """

        # Process predicted aggregation operators
        agg_ops = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3:"COUNT"}

        # Structure aggregations into an array
        aggreg = [
            agg_ops[x] for x in operators
        ]

        # Process predicted table cell coordinates
        answers = []

        # Mash coordinates into a single array.  This deals with multiple
        # question cases, but the query case wouldn't result in that
        # anyway, so more complex than it needs to be
        for coord in coords:
            if len(coord) == 1:
                # 1 cell
                answers.append(self.table.iat[coord[0]])
            else:
                # > 1 cell
                cell_values = []
                for coordinate in coord:
                    cell_values.append(self.table.iat[coordinate])
                answers.append(", ".join(cell_values))
      
        # Return values
        return aggreg, answers, coords

