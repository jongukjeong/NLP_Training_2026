import pandas as pd


df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
rows_before = len(df)

print("처리 전 데이터")
print(df)

df = df.dropna(subset=["text"])
df["text"] = df["text"].str.strip()
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)
df = df[df["text"] != ""]

df["label"] = df["label"].fillna("unknown")
df["label"] = df["label"].str.lower()

df = df.drop_duplicates(subset=["text"])
df["text_length"] = df["text"].str.len()

print("\n처리 후 데이터")
print(df)
print("\n처리 전 행 수:", rows_before)
print("처리 후 행 수:", len(df))
print("제거한 행 수:", rows_before - len(df))

df.to_csv("reviews_clean.csv", index=False, encoding="utf-8-sig")
print("저장 완료: reviews_clean.csv")
