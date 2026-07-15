import pandas as pd


df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
df = df.dropna(subset=["text"])
df["text"] = df["text"].str.strip()
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)
df = df[df["text"] != ""]
df["label"] = df["label"].fillna("unknown")
df["label"] = df["label"].str.lower()

print("중복 제거 전:", len(df))
df = df.drop_duplicates(subset=["text"])
print("중복 제거 후:", len(df))
print(df)
