import json
import os
from pathlib import Path
import pandas as pd
from transformers import AutoModel, AutoTokenizer, pipeline

BASE_DIR = Path(__file__).resolve().parent
MODEL_ID = os.getenv("HF_MODEL_ID", "klue/bert-base")


def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModel.from_pretrained(MODEL_ID)
    fill_mask = pipeline("fill-mask", model=MODEL_ID, tokenizer=MODEL_ID, device=-1)
    df = pd.read_csv(BASE_DIR / "prompts.csv", encoding="utf-8-sig")
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    rows = []
    for item in df.itertuples(index=False):
        text = item.text.replace("<MASK>", tokenizer.mask_token)
        predictions = fill_mask(text, top_k=5)
        rows.append({"id": item.id, "input": text, "predictions": [{"token": p["token_str"], "score": float(p["score"])} for p in predictions]})
    report = {"model_id": MODEL_ID, "model_type": model.config.model_type, "vocabulary_size": tokenizer.vocab_size, "results": rows}
    (out / "predictions.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"); print({k: report[k] for k in ("model_id", "model_type", "vocabulary_size")})


if __name__ == "__main__": main()
