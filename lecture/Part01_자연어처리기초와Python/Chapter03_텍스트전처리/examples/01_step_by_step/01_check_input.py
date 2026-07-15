import re

texts = [
    "  배송이   빨라요!!!  ",
    "문의: test@example.com",
    "자세한 내용은 https://example.com 에서 확인하세요.",
]

for text in texts:
    print("원문:", repr(text))
