import json
import os
import sys
from pathlib import Path
from retriever import PolicyRetriever

BASE_DIR = Path(__file__).resolve().parents[1]


def generated_answer(query, results):
    if not os.getenv("OPENAI_API_KEY"): return results[0]["content"]
    from openai import OpenAI
    context = "\n".join(f"[{r['document_id']}] {r['content']}" for r in results)
    response = OpenAI().responses.create(model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"), instructions="제공된 근거만 사용해 한국어로 답하세요. 근거가 부족하면 모른다고 말하고 문서 ID를 인용하세요.", input=f"질문: {query}\n근거:\n{context}")
    return response.output_text


def main():
    query = " ".join(sys.argv[1:]).strip() or "배송비는 얼마인가요?"
    results = PolicyRetriever(BASE_DIR / "data" / "knowledge.csv").search(query, 3)
    if not results or results[0]["score"] < 0.05:
        record = {"query": query, "answer": "관련 근거를 찾지 못했습니다. 담당자에게 확인해 주세요.", "sources": []}
    else:
        record = {"query": query, "answer": generated_answer(query, results), "sources": [{"document_id": r["document_id"], "source": r["source"], "version": r["version"], "score": r["score"]} for r in results]}
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True); (out / "last_response.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"); print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
