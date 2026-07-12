import json
import os
from pathlib import Path
import pandas as pd
import ollama

BASE_DIR = Path(__file__).resolve().parent
MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")


def main():
    df = pd.read_csv(BASE_DIR / "prompts.csv", encoding="utf-8-sig")
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    with (out / "responses.jsonl").open("w", encoding="utf-8") as file:
        for row in df.itertuples(index=False):
            response = ollama.generate(model=MODEL, prompt=row.prompt, options={"temperature": 0})
            record = {"id": row.id, "model": MODEL, "response": response["response"], "total_duration": response.get("total_duration"), "prompt_eval_count": response.get("prompt_eval_count"), "eval_count": response.get("eval_count")}
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(row.id, record["response"])


if __name__ == "__main__": main()
