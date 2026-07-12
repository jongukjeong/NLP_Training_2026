import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent


class Assistant:
    def __init__(self):
        self.faq = pd.read_csv(BASE_DIR / "faq.csv", encoding="utf-8-sig"); self.orders = pd.read_csv(BASE_DIR / "orders.csv", encoding="utf-8-sig", dtype=str)
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5)); self.matrix = self.vectorizer.fit_transform(self.faq["question"])
    def order_status(self, order_id):
        rows = self.orders[self.orders["order_id"] == order_id]
        return {"found": False} if rows.empty else {"found": True, "order_id": order_id, "status": rows.iloc[0]["status"]}
    def search_faq(self, query):
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel(); i = int(scores.argmax())
        return {"question": self.faq.iloc[i]["question"], "answer": self.faq.iloc[i]["answer"], "score": float(scores[i])}
    def run(self, query):
        match = re.search(r"ORD-\d{4}", query.upper()); tool = "order_status" if match else "search_faq"; result = self.order_status(match.group()) if match else self.search_faq(query)
        return {"query": query, "tool": tool, "result": result, "timestamp": datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("query", nargs="?", default="ORD-1001 배송 상태를 알려 주세요"); args = parser.parse_args()
    record = Assistant().run(args.query); out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    with (out / "audit.jsonl").open("a", encoding="utf-8") as file: file.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
