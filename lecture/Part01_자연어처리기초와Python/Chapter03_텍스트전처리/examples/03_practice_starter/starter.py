# Chapter 3 텍스트 전처리 Practice Starter

import re

texts = [
    "  배송이   빨라요!!!  ",
    "문의: test@example.com",
    "자세한 내용은 https://example.com 에서 확인하세요.",
]

print("입력을 먼저 확인하세요.")
for text in texts:
    print("원문:", repr(text))

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# URL 또는 이메일을 `[LINK]`, `[EMAIL]`로 바꾸는 규칙을 하나 추가하세요.
