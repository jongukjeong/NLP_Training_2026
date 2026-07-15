import pandas as pd


df = pd.read_csv("reviews.csv", encoding="utf-8-sig")

print(df)
print("행 수:", len(df))
print("열 이름:", df.columns.tolist())
