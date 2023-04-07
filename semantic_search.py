
"""
Defines SemanticSearch which implements a sub-model lookup for a
natural language question.  A body of knowledge is provided as questions
mapped to sub-models.  When a query is presented, its embedding is used
to find the closes question, and that questions sub-model is used to
respond to the question.

There's a fair amount of doing 'approximately' the right here.  If the
vector space is initialised from document titles, then we're hoping that
the questions and document titles are close enough to meet the closes-match
algorithm.

Example:

    # Create model
    ss = SemanticSearch.create()
   
    # Add knowledge
    pizza = requests.get("https://en.wikipedia.org/wiki/Pizza").text

    # Add knowledge
    ss.add(
        "How big is the world's largest pizza?",
        TextQuery.create(pizza)
    )

    # Add knowledge
    ss.add(
        "How do you make Pizza?",
        TextQuery.create(pizza)
    )

    # Query map
    ans = ss.query("What is the world's biggest pizza?")
    for an in ans:
        an.show()

Uses the Embedding class, which uses the
sentence-transformers/all-MiniLM-L6-v2 model to map sentences to vector space.
"""

from scipy import spatial
from embedding import Embedding

class SemanticSearch:
    """
    Sub-model lookup for a natural language question.
    """

    @staticmethod
    def create():
        "Returns an empty vector space"
        return SemanticSearch()

    def __init__(self):
        "Returns an empty vector space"
        self.vecs = []
        self.nodes = []
        self.embedding = Embedding()
        self.tree = None

    def add(self, title, node):
        "Adds a sub-model to the semantic search space"

        # Fetch embedding from the question / model title
        emb = self.embedding.get(title)

        # Add embedding and sub-model to lists
        self.vecs.append(emb)
        self.nodes.append(node)

        # 'tree' is a vector space search construct which is created from
        # all embeddings at query time.  If new sub-models are added,
        # this clears out the tree.
        self.tree = None

    def query(self, q):
        """
        Looks up a sub-model using the supplied question.  Invokes the
        closest matching sub-model, using the supplied question.
        """

        # You can't query empty vector space
        if len(self.vecs) == 0:
            raise RuntimeError("No nodes to query")

        # Initialise the vector search query from questions / document
        # titles if the search construct is in an uninitialised state
        if self.tree == None:
            self.tree = spatial.KDTree(self.vecs)

        # Compute an embedding on the question
        emb = self.embedding.get(q)

        # Find closest vector to that embedding
        result = self.tree.query(emb)

        # The found vector is mapped to a sub-model
        ix = result[1]
        node = self.nodes[ix]

        # Execute the query on the sub-model and return results
        return node.query(q)
