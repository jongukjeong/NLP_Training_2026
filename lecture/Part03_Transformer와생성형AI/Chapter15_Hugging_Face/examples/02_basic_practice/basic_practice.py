# Chapter 15 Hugging Face Basic Practice

model_cards = [
    {"name": "sentiment-ko", "task": "sentiment", "language": "ko"},
    {"name": "summary-en", "task": "summary", "language": "en"},
    {"name": "qa-ko", "task": "question-answering", "language": "ko"},
]
wanted_task = "sentiment"

print("=== 입력 확인 ===")
for card in model_cards:
    print(card)

print("\n=== 핵심 처리 ===")
selected_models = []
for card in model_cards:
    if card["task"] == wanted_task and card["language"] == "ko":
        selected_models.append(card["name"])

print("\n=== 결과 확인 ===")
print("원하는 task:", wanted_task)
print("선택 가능한 모델:", selected_models)
