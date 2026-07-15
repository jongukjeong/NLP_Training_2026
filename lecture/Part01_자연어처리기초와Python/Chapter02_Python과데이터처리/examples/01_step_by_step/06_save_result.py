import pandas as pd


df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
rows_before = len(df)

df = df.dropna(subset=["text"])
df["text"] = df["text"].str.strip()
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)
df = df[df["text"] != ""]
df["label"] = df["label"].fillna("unknown")
df["label"] = df["label"].str.lower()
df = df.drop_duplicates(subset=["text"])

df.to_csv("reviews_clean.csv", index=False, encoding="utf-8-sig")

print("처리 전:", rows_before)
print("처리 후:", len(df))
print("저장 완료: reviews_clean.csv")
