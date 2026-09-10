"""
rag.py
------
A simple Retrieval-Augmented Generation (RAG) module for the AI IT Helpdesk Agent.

This module:
1. Loads the knowledge base text file.
2. Splits it into category-based chunks (sections).
3. Converts the chunks into TF-IDF vectors.
4. Compares a user query against the chunks using cosine similarity.
5. Returns the most relevant chunk(s), or a "not found" signal if nothing matches well.

No external LLM or API is used. Everything runs locally using scikit-learn.
"""

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_KB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "knowledge_base", "troubleshooting.txt"
)

# Below this similarity score, we treat the knowledge base as "not confident enough"
# and tell the user honestly rather than guessing.
SIMILARITY_THRESHOLD = 0.08


class KnowledgeBaseError(Exception):
    """Raised when the knowledge base file cannot be loaded or is empty."""
    pass


class SimpleRAG:
    """
    A minimal TF-IDF + cosine-similarity based retriever over a plain-text
    knowledge base. Each "CATEGORY:" block in the knowledge base file is
    treated as one retrievable chunk/document.
    """

    def __init__(self, kb_path: str = DEFAULT_KB_PATH):
        self.kb_path = kb_path
        self.categories = []      # e.g. ["Wi-Fi and Internet Issues", ...]
        self.chunks = []          # full text of each chunk
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_and_index()

    # ------------------------------------------------------------------
    # Loading and indexing
    # ------------------------------------------------------------------
    def _load_and_index(self):
        if not os.path.exists(self.kb_path):
            raise KnowledgeBaseError(
                f"Knowledge base file not found at '{self.kb_path}'. "
                "Please make sure knowledge_base/troubleshooting.txt exists."
            )

        with open(self.kb_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        if not raw_text.strip():
            raise KnowledgeBaseError("Knowledge base file is empty.")

        self._split_into_chunks(raw_text)

        if not self.chunks:
            raise KnowledgeBaseError("No valid CATEGORY sections found in knowledge base.")

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.chunks)

    def _split_into_chunks(self, raw_text: str):
        """Splits the knowledge base into chunks, one per 'CATEGORY:' block."""
        blocks = raw_text.split("CATEGORY:")
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            lines = block.splitlines()
            category_name = lines[0].strip() if lines else "Uncategorized"
            full_chunk_text = "CATEGORY: " + block
            self.categories.append(category_name)
            self.chunks.append(full_chunk_text)

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = 1):
        """
        Retrieve the most relevant knowledge-base chunk(s) for a query.

        Returns a list of dicts:
            {"category": str, "content": str, "score": float}
        Returns an empty list if the query is empty or nothing is relevant
        enough (score below SIMILARITY_THRESHOLD).
        """
        if not query or not query.strip():
            return []

        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        except Exception:
            # Retrieval failure should never crash the agent.
            return []

        ranked_indices = similarities.argsort()[::-1]

        results = []
        for idx in ranked_indices[:top_k]:
            score = float(similarities[idx])
            if score < SIMILARITY_THRESHOLD:
                continue
            results.append({
                "category": self.categories[idx],
                "content": self.chunks[idx],
                "score": score,
            })

        return results

    def is_covered(self, query: str) -> bool:
        """Quick check: does the knowledge base have anything relevant to this query?"""
        return len(self.retrieve(query, top_k=1)) > 0


if __name__ == "__main__":
    # Simple manual test when running `python rag.py` directly.
    rag = SimpleRAG()
    test_queries = [
        "My Wi-Fi is connected but I don't have internet.",
        "My printer is not printing.",
        "My computer is running very slowly.",
        "I forgot my password and cannot login.",
        "My laptop has an unknown alien problem.",
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = rag.retrieve(q)
        if results:
            for r in results:
                print(f"  -> Category: {r['category']} (score={r['score']:.3f})")
        else:
            print("  -> No relevant knowledge base entry found.")
