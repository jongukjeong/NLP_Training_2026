import pandas as pd


# 1. CSV 파일을 읽으세요.
df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
rows_before = len(df)

# 2. text가 결측인 행을 제거하세요.

# 3. text의 앞뒤 공백과 연속 공백을 정리하세요.

# 4. 빈 문자열인 행을 제거하세요.

# 5. label의 결측값을 unknown으로 채우고 소문자로 바꾸세요.

# 6. text가 같은 중복 행을 제거하세요.

# 7. text_length 열을 추가하세요.

# 8. 처리 전후 행 수를 출력하세요.
print("처리 전 행 수:", rows_before)
print("처리 후 행 수:", len(df))

# 9. 레이블별 문장 수를 출력하세요.

# 10. reviews_clean.csv로 저장하세요.
