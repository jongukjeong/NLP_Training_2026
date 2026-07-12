import json
from pathlib import Path
import pandas as pd
from retriever import PolicyRetriever

BASE_DIR = Path(__file__).resolve().parents[1]


def main():
    retriever = PolicyRetriever(BASE_DIR / "data" / "knowledge.csv")
    evaluation = pd.read_csv(BASE_DIR / "data" / "evaluation.csv", encoding="utf-8-sig", dtype=str)
    ranks, rows = [], []
    for item in evaluation.itertuples(index=False):
        results = retriever.search(item.query, top_k=3); ids = [r["document_id"] for r in results]
        rank = ids.index(item.relevant_id) + 1 if item.relevant_id in ids else None; ranks.append(rank)
        rows.append({"query": item.query, "relevant_id": item.relevant_id, "rank": rank, "retrieved_ids": "|".join(ids)})
    count = len(ranks); report = {"queries": count, "hit_at_1": sum(r == 1 for r in ranks) / count, "hit_at_3": sum(r is not None and r <= 3 for r in ranks) / count, "mrr": sum(0 if r is None else 1 / r for r in ranks) / count}
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True); pd.DataFrame(rows).to_csv(out / "retrieval_results.csv", index=False, encoding="utf-8-sig"); (out / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8"); print(report)


if __name__ == "__main__": main()
