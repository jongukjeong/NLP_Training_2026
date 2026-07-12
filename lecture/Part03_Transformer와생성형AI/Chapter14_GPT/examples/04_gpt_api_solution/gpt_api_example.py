import json
import os
from pathlib import Path
import pandas as pd
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY 환경변수를 설정하세요.")
    client = OpenAI()
    df = pd.read_csv(BASE_DIR / "questions.csv", encoding="utf-8-sig")
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    with (out / "responses.jsonl").open("w", encoding="utf-8") as file:
        for row in df.itertuples(index=False):
            response = client.responses.create(
                model=MODEL,
                instructions="고객지원 답변 초안을 한국어 두 문장 이내로 작성하세요. 확인되지 않은 정책은 단정하지 마세요.",
                input=str(row.question),
            )
            record = {"id": row.id, "model": MODEL, "question": row.question, "answer": response.output_text, "response_id": response.id}
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(row.id, response.output_text)


if __name__ == "__main__": main()
