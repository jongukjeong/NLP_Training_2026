model_cards = [
    {"name": "sentiment-ko", "task": "sentiment", "language": "ko"},
    {"name": "summary-en", "task": "summary", "language": "en"},
    {"name": "qa-ko", "task": "question-answering", "language": "ko"},
]
wanted_task = "sentiment"

for card in model_cards:
    print(card)
