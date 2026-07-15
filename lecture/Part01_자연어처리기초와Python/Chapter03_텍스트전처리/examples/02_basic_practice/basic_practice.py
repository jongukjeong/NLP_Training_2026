# Chapter 3 텍스트 전처리 Basic Practice

import re

texts = [
    "  배송이   빨라요!!!  ",
    "문의: test@example.com",
    "자세한 내용은 https://example.com 에서 확인하세요.",
]

print("=== 입력 확인 ===")
for text in texts:
    print("원문:", repr(text))

print("\n=== 핵심 처리 ===")
cleaned_texts = []
for text in texts:
    cleaned = text.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[!]{2,}", "!", cleaned)
    cleaned_texts.append(cleaned)

print("\n=== 결과 확인 ===")
for before, after in zip(texts, cleaned_texts):
    print("전:", before)
    print("후:", after)
    print()
