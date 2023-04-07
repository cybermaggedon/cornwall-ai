
# Cornwall AI

## Overview

Very simple bit of AI code, answers a few basic questions using data
contained in this repo.

The AI has three components:
- A semantic component which matches a question to a sub-model based
  on sentence analysis.
- A question answering component which takes a question and answers it
  using contextual text.
- A question answering component which takes a question and answers it
  using tables of text.

## Running it

You need to install:
- Python 3
- Pandas: `pip3 install pandas`
- Transformers: `pip3 install transformers
- Tabulate: `pip3 install tabulate`
- PyTorch: `pip3 install pytorch`
- scipy: `pip3 install scipy`
- sentence_transformers: `pip3 install sentence_transformers`

And then run `cornwall-ai`.  The first time it runs, it downloads a few
large models.  After that, the models are cached.

```
[cornwall-ai]$ ./cornwall-ai
Loading...
Asking questions...

Q: Which county is Bude in?
A: Cornwall, England

Q: What is the county town of Cornwall?
A: Redruth

+---------+------------+
|  town   | population |
+---------+------------+
| Redruth |   42690    |
+---------+------------+

Q: How do you make a souffle?
A: beaten egg whites

Q: How do you start a revolution?
A: population revolts against the government

Q: What is the population of Helston in Cornwall
A: 12184

+---------+------------+
|  town   | population |
+---------+------------+
| Helston |   12184    |
+---------+------------+

Q: Which Cornish towns have populations more than 20000?
A: Redruth, Falmouth, St Austell, Truro, Newquay

+------------+------------+
|    town    | population |
+------------+------------+
|  Redruth   |   42690    |
|  Falmouth  |   31988    |
| St Austell |   25447    |
|   Truro    |   23041    |
|  Newquay   |   20189    |
+------------+------------+
```

## Data

The data is in the data directory, all copy/pasted from Wikipedia.
One of the files is a CSV of town populations from the 2011 census.


## Models

The models are all from Hugging Face:
- https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- https://huggingface.co/google/tapas-large-finetuned-wtq
- https://huggingface.co/distilbert-base-cased-distilled-squad

## Further reading

TAPAS:
- https://www.aclweb.org/anthology/2020.acl-main.398
- https://www.aclweb.org/anthology/2020.findings-emnlp.27/

DistilBERT:
- https://medium.com/huggingface/distilbert-8cf3380435b5

