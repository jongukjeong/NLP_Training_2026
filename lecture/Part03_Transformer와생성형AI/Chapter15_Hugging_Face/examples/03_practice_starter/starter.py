# Chapter 15 Hugging Face Practice Starter

model_cards = [
    {"name": "sentiment-ko", "task": "sentiment", "language": "ko"},
    {"name": "summary-en", "task": "summary", "language": "en"},
    {"name": "qa-ko", "task": "question-answering", "language": "ko"},
]
wanted_task = "sentiment"

print("입력을 먼저 확인하세요.")
for card in model_cards:
    print(card)

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# wanted_task를 바꾸고 언어와 task가 모두 맞는 모델만 선택되는지 확인하세요.
