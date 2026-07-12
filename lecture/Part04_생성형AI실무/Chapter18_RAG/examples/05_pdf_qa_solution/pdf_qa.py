import json
from pathlib import Path
import pandas as pd
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent


def main():
    pdf = BASE_DIR / "policy.pdf"
    if not pdf.exists(): raise FileNotFoundError("먼저 build_sample_pdf.py를 실행하세요.")
    pages = [{"page": i + 1, "text": page.extract_text() or ""} for i, page in enumerate(PdfReader(pdf).pages)]
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5)); matrix = vectorizer.fit_transform([p["text"] for p in pages])
    evaluation, rows = pd.read_csv(BASE_DIR / "evaluation.csv", encoding="utf-8-sig"), []
    for item in evaluation.itertuples(index=False):
        scores = cosine_similarity(vectorizer.transform([item.question]), matrix).ravel(); best = int(scores.argmax()); page = pages[best]
        rows.append({"question": item.question, "expected_page": item.page, "retrieved_page": page["page"], "score": float(scores[best]), "answer": page["text"].strip(), "source": f"policy.pdf#page={page['page']}"})
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True); pd.DataFrame(rows).to_csv(out / "answers.csv", index=False, encoding="utf-8-sig")
    report = {"questions": len(rows), "page_accuracy": sum(r["expected_page"] == r["retrieved_page"] for r in rows) / len(rows)}
    (out / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8"); print(report)


if __name__ == "__main__": main()
