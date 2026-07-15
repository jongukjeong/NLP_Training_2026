import pandas as pd


df = pd.read_csv("reviews.csv", encoding="utf-8-sig")

print("결측값 제거 전:", len(df))
df = df.dropna(subset=["text"])
print("결측값 제거 후:", len(df))
print(df)
