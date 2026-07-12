from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PolicyRetriever:
    def __init__(self, knowledge_path: Path):
        self.documents = pd.read_csv(knowledge_path, encoding="utf-8-sig", dtype=str)
        required = {"document_id", "title", "content", "source", "version", "access_level"}
        if missing := required - set(self.documents.columns): raise ValueError(f"필수 열 누락: {sorted(missing)}")
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=1)
        self.matrix = self.vectorizer.fit_transform((self.documents["title"] + " " + self.documents["content"]).tolist())

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not query.strip(): return []
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel()
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], self.documents.iloc[i]["document_id"]))[:top_k]
        return [{**self.documents.iloc[i].to_dict(), "score": float(scores[i])} for i in order]
