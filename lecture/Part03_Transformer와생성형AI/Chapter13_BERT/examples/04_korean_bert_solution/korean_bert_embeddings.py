import json
import os
from pathlib import Path
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer

BASE_DIR = Path(__file__).resolve().parent
MODEL_ID = os.getenv("HF_BERT_MODEL", "klue/bert-base")


def main():
    df = pd.read_csv(BASE_DIR / "sentences.csv", encoding="utf-8-sig")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModel.from_pretrained(MODEL_ID); model.eval()
    inputs = tokenizer(df["text"].tolist(), padding=True, truncation=True, max_length=64, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**inputs).last_hidden_state
    mask = inputs["attention_mask"].unsqueeze(-1)
    embeddings = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1)
    similarity = cosine_similarity(embeddings.numpy())
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    pd.DataFrame(similarity, index=df["id"], columns=df["id"]).to_csv(out / "similarity.csv", encoding="utf-8-sig")
    report = {"model_id": MODEL_ID, "sentences": len(df), "embedding_dimension": int(embeddings.shape[1])}
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"); print(report)


if __name__ == "__main__": main()
