import json
import os
from pathlib import Path
import pandas as pd
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
ALLOWED = {"delivery", "refund", "account", "other"}

PROMPTS = {
    "zero_shot": "문의 category를 delivery, refund, account, other 중 하나로 분류하고 JSON만 출력하세요. 형식: {\"category\": \"...\"}",
    "few_shot": "문의 category를 분류해 JSON만 출력하세요. 배송이 늦어요→{\"category\":\"delivery\"}, 돈을 돌려받고 싶어요→{\"category\":\"refund\"}, 로그인이 안 돼요→{\"category\":\"account\"}",
}


def main():
    if not os.getenv("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY를 설정하세요.")
    client, data, rows = OpenAI(), pd.read_csv(BASE_DIR / "evaluation.csv", encoding="utf-8-sig"), []
    for version, instruction in PROMPTS.items():
        correct = valid = 0
        for item in data.itertuples(index=False):
            response = client.responses.create(model=MODEL, instructions=instruction, input=item.text)
            try:
                category = json.loads(response.output_text)["category"]; valid += category in ALLOWED; correct += category == item.label
            except (json.JSONDecodeError, KeyError, TypeError): category = None
            rows.append({"version": version, "text": item.text, "expected": item.label, "predicted": category})
        print(version, {"accuracy": correct / len(data), "schema_rate": valid / len(data)})
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True); pd.DataFrame(rows).to_csv(out / "results.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__": main()
