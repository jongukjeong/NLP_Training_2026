import re

texts = [
    "  배송이   빨라요!!!  ",
    "문의: test@example.com",
    "자세한 내용은 https://example.com 에서 확인하세요.",
]

for text in texts:
    print("원문:", repr(text))

cleaned_texts = []
for text in texts:
    cleaned = text.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"[!]{2,}", "!", cleaned)
    cleaned_texts.append(cleaned)

for before, after in zip(texts, cleaned_texts):
    print("전:", before)
    print("후:", after)
    print()
