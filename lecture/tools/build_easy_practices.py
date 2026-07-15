from pathlib import Path


LECTURE_DIR = Path(__file__).resolve().parent.parent


CHAPTERS = [
    {
        "path": "Part01_자연어처리기초와Python/Chapter03_텍스트전처리",
        "title": "Chapter 3 텍스트 전처리",
        "input": '''import re

texts = [
    "  배송이   빨라요!!!  ",
    "문의: test@example.com",
    "자세한 내용은 https://example.com 에서 확인하세요.",
]''',
        "show": 'for text in texts:\n    print("원문:", repr(text))',
        "core": '''cleaned_texts = []
for text in texts:
    cleaned = text.strip()
    cleaned = re.sub(r"\\s+", " ", cleaned)
    cleaned = re.sub(r"[!]{2,}", "!", cleaned)
    cleaned_texts.append(cleaned)''',
        "result": 'for before, after in zip(texts, cleaned_texts):\n    print("전:", before)\n    print("후:", after)\n    print()',
        "challenge": "URL 또는 이메일을 `[LINK]`, `[EMAIL]`로 바꾸는 규칙을 하나 추가하세요.",
    },
    {
        "path": "Part01_자연어처리기초와Python/Chapter04_텍스트의수치화",
        "title": "Chapter 4 텍스트의 수치화",
        "input": '''from collections import Counter

documents = [
    "배송이 빠르고 포장이 좋아요",
    "배송이 늦어서 환불하고 싶어요",
    "상품 품질이 정말 좋아요",
]''',
        "show": 'for number, document in enumerate(documents, 1):\n    print(number, document)',
        "core": '''word_counts = []
for document in documents:
    words = document.split()
    word_counts.append(Counter(words))''',
        "result": 'for number, counts in enumerate(word_counts, 1):\n    print(number, dict(counts))\n\nquery = "배송이 늦어요"\nquery_words = set(query.split())\nfor number, document in enumerate(documents, 1):\n    score = len(query_words & set(document.split()))\n    print(number, "검색 점수:", score)',
        "challenge": "질문을 바꾸고 가장 높은 검색 점수의 문서를 찾으세요.",
    },
    {
        "path": "Part01_자연어처리기초와Python/Chapter05_단어임베딩",
        "title": "Chapter 5 단어 임베딩",
        "input": '''import math

vectors = {
    "배송": [0.9, 0.1],
    "택배": [0.8, 0.2],
    "환불": [0.1, 0.9],
    "반품": [0.2, 0.8],
}''',
        "show": 'for word, vector in vectors.items():\n    print(word, vector)',
        "core": '''def cosine(a, b):
    dot = a[0] * b[0] + a[1] * b[1]
    length_a = math.sqrt(a[0] ** 2 + a[1] ** 2)
    length_b = math.sqrt(b[0] ** 2 + b[1] ** 2)
    return dot / (length_a * length_b)''',
        "result": 'target = "배송"\nfor word in vectors:\n    if word != target:\n        score = cosine(vectors[target], vectors[word])\n        print(target, "↔", word, round(score, 3))',
        "challenge": "새 단어와 2차원 벡터를 추가하고 가장 비슷한 단어를 찾으세요.",
    },
    {
        "path": "Part02_딥러닝기반자연어처리/Chapter06_TensorFlow와Keras",
        "title": "Chapter 6 TensorFlow와 Keras",
        "input": '''samples = [
    [1.0, 0.0],
    [0.8, 0.2],
    [0.1, 0.9],
]
weights = [0.7, -0.4]
bias = 0.1''',
        "show": 'print("샘플 수:", len(samples))\nprint("특징 수:", len(samples[0]))\nprint("첫 샘플:", samples[0])',
        "core": '''predictions = []
for sample in samples:
    score = sample[0] * weights[0] + sample[1] * weights[1] + bias
    predictions.append(score)''',
        "result": 'for sample, score in zip(samples, predictions):\n    print(sample, "→", round(score, 2))',
        "challenge": "weights 값 하나를 바꾸고 예측 점수가 어떻게 달라지는지 확인하세요.",
    },
    {
        "path": "Part02_딥러닝기반자연어처리/Chapter07_딥러닝기초",
        "title": "Chapter 7 딥러닝 기초",
        "input": '''sentences = [
    ("배송이 빠르고 좋아요", 1),
    ("환불이 늦고 불편해요", 0),
    ("상품이 정말 좋아요", 1),
]
weights = {"좋아요": 2, "빠르고": 1, "늦고": -1, "불편해요": -2}''',
        "show": 'for sentence, label in sentences:\n    print("문장:", sentence, "정답:", label)',
        "core": '''results = []
for sentence, label in sentences:
    score = 0
    for word in sentence.split():
        score += weights.get(word, 0)
    prediction = 1 if score > 0 else 0
    results.append((sentence, label, score, prediction))''',
        "result": 'for sentence, label, score, prediction in results:\n    print(sentence, "점수:", score, "예측:", prediction, "정답:", label)',
        "challenge": "오분류 문장이 생기도록 문장을 추가하고 가중치를 조정하세요.",
    },
    {
        "path": "Part02_딥러닝기반자연어처리/Chapter08_순환신경망_RNN",
        "title": "Chapter 8 순환신경망 RNN",
        "input": '''tokens = ["배송", "정말", "빨라요"]
token_values = {"배송": 0.2, "정말": 0.5, "빨라요": 0.9}''',
        "show": 'for position, token in enumerate(tokens, 1):\n    print(position, token, token_values[token])',
        "core": '''hidden = 0.0
history = []
for token in tokens:
    hidden = 0.5 * hidden + token_values[token]
    history.append((token, hidden))''',
        "result": 'for token, hidden in history:\n    print(token, "후 hidden state:", round(hidden, 3))\nprint("최종 상태:", round(hidden, 3))',
        "challenge": "토큰 순서를 바꾸고 최종 hidden state가 달라지는지 확인하세요.",
    },
    {
        "path": "Part02_딥러닝기반자연어처리/Chapter09_LSTM과GRU",
        "title": "Chapter 9 LSTM과 GRU",
        "input": '''values = [0.2, 0.9, -0.4, 0.8]
forget_gate = 0.8
input_gate = 0.6''',
        "show": 'print("문장 값:", values)\nprint("기억 유지 비율:", forget_gate)',
        "core": '''memory = 0.0
memory_history = []
for value in values:
    memory = forget_gate * memory + input_gate * value
    memory_history.append(memory)''',
        "result": 'for step, memory in enumerate(memory_history, 1):\n    print(step, "번째 기억:", round(memory, 3))',
        "challenge": "forget_gate를 0.2와 0.9로 바꿔 오래된 정보가 얼마나 남는지 비교하세요.",
    },
    {
        "path": "Part02_딥러닝기반자연어처리/Chapter10_Seq2Seq와Encoder_Decoder",
        "title": "Chapter 10 Seq2Seq와 Encoder-Decoder",
        "input": '''source_sentence = "나는 학생 입니다"
dictionary = {"나는": "I", "학생": "student", "입니다": "am"}''',
        "show": 'source_tokens = source_sentence.split()\nprint("입력 토큰:", source_tokens)',
        "core": '''encoded = source_tokens
decoded = []
for token in encoded:
    decoded.append(dictionary.get(token, "[UNK]"))''',
        "result": 'print("Encoder 결과:", encoded)\nprint("Decoder 결과:", decoded)\nprint("출력 문장:", " ".join(decoded))',
        "challenge": "사전에 단어를 추가하고 새로운 짧은 문장을 변환하세요.",
    },
    {
        "path": "Part03_Transformer와생성형AI/Chapter11_Attention_Mechanism",
        "title": "Chapter 11 Attention",
        "input": '''import math

tokens = ["배송", "정말", "빨라요"]
scores = [1.0, 0.5, 2.0]''',
        "show": 'for token, score in zip(tokens, scores):\n    print(token, "유사도:", score)',
        "core": '''exp_scores = [math.exp(score) for score in scores]
total = sum(exp_scores)
weights = [value / total for value in exp_scores]''',
        "result": 'for token, weight in zip(tokens, weights):\n    print(token, "Attention:", round(weight, 3))\nprint("가중치 합:", round(sum(weights), 3))',
        "challenge": "scores 중 하나를 크게 바꾸고 Attention이 어디에 집중하는지 확인하세요.",
    },
    {
        "path": "Part03_Transformer와생성형AI/Chapter12_Transformer",
        "title": "Chapter 12 Transformer",
        "input": '''token_vector = [0.2, 0.7, -0.1]
attention_output = [0.4, -0.2, 0.3]''',
        "show": 'print("입력 벡터:", token_vector)\nprint("Attention 출력:", attention_output)',
        "core": '''residual = []
for original, attention in zip(token_vector, attention_output):
    residual.append(original + attention)

activated = [max(0, value) for value in residual]''',
        "result": 'print("잔차 연결 후:", residual)\nprint("활성화 후:", activated)\nprint("shape:", len(activated))',
        "challenge": "벡터 값을 바꾸고 잔차 연결이 원래 정보를 어떻게 보존하는지 설명하세요.",
    },
    {
        "path": "Part03_Transformer와생성형AI/Chapter13_BERT",
        "title": "Chapter 13 BERT",
        "input": '''sentence = "배송이 [MASK] 도착했어요"
vocabulary = {"빨리": 0.7, "늦게": 0.2, "안전하게": 0.1}''',
        "show": 'tokens = sentence.split()\nprint("토큰:", tokens)\nprint("MASK 위치:", tokens.index("[MASK]"))',
        "core": '''best_word = ""
best_score = -1.0
for word, score in vocabulary.items():
    if score > best_score:
        best_word = word
        best_score = score''',
        "result": 'completed = sentence.replace("[MASK]", best_word)\nprint("후보:", vocabulary)\nprint("선택:", best_word)\nprint("완성 문장:", completed)',
        "challenge": "후보 단어와 점수를 바꿔 MASK 결과를 비교하세요.",
    },
    {
        "path": "Part03_Transformer와생성형AI/Chapter14_GPT",
        "title": "Chapter 14 GPT",
        "input": '''prompt = "고객에게 배송 지연을"
next_tokens = {"안내합니다": 0.55, "사과합니다": 0.35, "무시합니다": 0.10}''',
        "show": 'print("Prompt:", prompt)\nprint("다음 토큰 후보:", next_tokens)',
        "core": '''selected = ""
highest = -1.0
for token, probability in next_tokens.items():
    if probability > highest:
        selected = token
        highest = probability''',
        "result": 'print("선택 토큰:", selected)\nprint("생성 결과:", prompt, selected)',
        "challenge": "Prompt에 말투나 출력 형식 조건을 추가하고 원하는 후보의 점수를 조정하세요.",
    },
    {
        "path": "Part03_Transformer와생성형AI/Chapter15_Hugging_Face",
        "title": "Chapter 15 Hugging Face",
        "input": '''model_cards = [
    {"name": "sentiment-ko", "task": "sentiment", "language": "ko"},
    {"name": "summary-en", "task": "summary", "language": "en"},
    {"name": "qa-ko", "task": "question-answering", "language": "ko"},
]
wanted_task = "sentiment"''',
        "show": 'for card in model_cards:\n    print(card)',
        "core": '''selected_models = []
for card in model_cards:
    if card["task"] == wanted_task and card["language"] == "ko":
        selected_models.append(card["name"])''',
        "result": 'print("원하는 task:", wanted_task)\nprint("선택 가능한 모델:", selected_models)',
        "challenge": "wanted_task를 바꾸고 언어와 task가 모두 맞는 모델만 선택되는지 확인하세요.",
    },
    {
        "path": "Part04_생성형AI실무/Chapter16_대규모언어모델_LLM",
        "title": "Chapter 16 대규모 언어모델",
        "input": '''models = [
    {"name": "small", "memory_gb": 4, "tokens_per_second": 35},
    {"name": "medium", "memory_gb": 10, "tokens_per_second": 18},
    {"name": "large", "memory_gb": 24, "tokens_per_second": 8},
]
available_memory = 12''',
        "show": 'print("사용 가능 메모리:", available_memory, "GB")\nfor model in models:\n    print(model)',
        "core": '''runnable = []
for model in models:
    if model["memory_gb"] <= available_memory:
        runnable.append(model)''',
        "result": 'for model in runnable:\n    seconds = 100 / model["tokens_per_second"]\n    print(model["name"], "실행 가능, 100토큰 예상", round(seconds, 1), "초")',
        "challenge": "메모리 값을 바꾸고 실행 가능한 모델과 속도의 trade-off를 설명하세요.",
    },
    {
        "path": "Part04_생성형AI실무/Chapter17_Prompt_Engineering",
        "title": "Chapter 17 Prompt Engineering",
        "input": '''prompts = [
    "배송 지연 안내문을 써줘",
    "고객에게 정중한 말투로 배송 지연 안내문을 3문장으로 써줘",
]
required_words = ["고객", "정중", "3문장"]''',
        "show": 'for number, prompt in enumerate(prompts, 1):\n    print(number, prompt)',
        "core": '''scores = []
for prompt in prompts:
    score = 0
    for word in required_words:
        if word in prompt:
            score += 1
    scores.append(score)''',
        "result": 'for prompt, score in zip(prompts, scores):\n    print("Prompt:", prompt)\n    print("명확성 점수:", score, "/", len(required_words))',
        "challenge": "대상, 말투, 길이, 출력 형식 중 하나를 추가하고 점수 기준도 수정하세요.",
    },
    {
        "path": "Part04_생성형AI실무/Chapter18_RAG",
        "title": "Chapter 18 RAG",
        "input": '''documents = [
    "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "비밀번호는 계정 설정에서 변경할 수 있습니다.",
]
question = "환불은 며칠 안에 신청하나요?"''',
        "show": 'print("질문:", question)\nfor number, document in enumerate(documents, 1):\n    print(number, document)',
        "core": '''question_words = set(question.replace("?", "").split())
scores = []
for document in documents:
    document_words = set(document.replace(".", "").split())
    scores.append(len(question_words & document_words))
best_index = scores.index(max(scores))''',
        "result": 'print("검색 점수:", scores)\nprint("선택 근거:", documents[best_index])\nprint("답변: 선택된 근거를 확인해 답변합니다.")',
        "challenge": "질문과 문서를 추가하고 검색 결과가 틀리는 사례를 하나 찾으세요.",
    },
    {
        "path": "Part04_생성형AI실무/Chapter19_AI_Agent와최신프레임워크",
        "title": "Chapter 19 AI Agent",
        "input": '''questions = [
    "주문 상태를 알려줘",
    "환불 규정을 알려줘",
    "내 비밀번호를 대신 바꿔줘",
]''',
        "show": 'for question in questions:\n    print("질문:", question)',
        "core": '''decisions = []
for question in questions:
    if "주문" in question:
        tool = "order_lookup"
    elif "규정" in question:
        tool = "faq_search"
    else:
        tool = "safe_stop"
    decisions.append((question, tool))''',
        "result": 'for question, tool in decisions:\n    print(question, "→", tool)',
        "challenge": "도구를 실행해도 되는 질문과 사용자 확인이 필요한 질문을 구분하세요.",
    },
    {
        "path": "Part04_생성형AI실무/Chapter20_최종프로젝트",
        "title": "Chapter 20 최종 프로젝트",
        "input": '''knowledge = {
    "배송": "배송 조회는 주문 내역에서 확인할 수 있습니다.",
    "환불": "환불은 상품 수령 후 7일 이내 신청할 수 있습니다.",
    "계정": "비밀번호는 계정 설정에서 변경할 수 있습니다.",
}
questions = ["배송은 어디서 조회하나요?", "환불 기간은 며칠인가요?"]''',
        "show": 'print("지식 문서 수:", len(knowledge))\nfor question in questions:\n    print("테스트 질문:", question)',
        "core": '''results = []
for question in questions:
    answer = "근거를 찾지 못했습니다."
    source = "없음"
    for keyword, document in knowledge.items():
        if keyword in question:
            answer = document
            source = keyword
            break
    results.append((question, answer, source))''',
        "result": 'for question, answer, source in results:\n    print("질문:", question)\n    print("답변:", answer)\n    print("근거:", source)\n    print()',
        "challenge": "지식 문서와 테스트 질문을 하나씩 추가하고 근거 없음 사례도 확인하세요.",
    },
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_chapter(config: dict[str, object]) -> None:
    chapter_dir = LECTURE_DIR / str(config["path"])
    title = str(config["title"])
    input_code = str(config["input"])
    show_code = str(config["show"])
    core_code = str(config["core"])
    result_code = str(config["result"])
    challenge = str(config["challenge"])

    step_dir = chapter_dir / "examples/01_step_by_step"
    basic_dir = chapter_dir / "examples/02_basic_practice"
    starter_dir = chapter_dir / "examples/03_practice_starter"

    write(step_dir / "01_check_input.py", f"{input_code}\n\n{show_code}")
    write(step_dir / "02_run_core.py", f"{input_code}\n\n{show_code}\n\n{core_code}\n\nprint('핵심 처리 완료')")
    write(step_dir / "03_check_result.py", f"{input_code}\n\n{show_code}\n\n{core_code}\n\n{result_code}")
    write(
        step_dir / "README.md",
        f"""# {title} Step by Step

표준 Python으로 핵심 흐름만 확인합니다. 완성형 solution의 라이브러리·모델·API 코드는 나중에 비교합니다.

1. `01_check_input.py`: 입력을 화면에서 확인
2. `02_run_core.py`: 핵심 처리 한 단계 실행
3. `03_check_result.py`: 결과를 입력과 비교

```powershell
python 01_check_input.py
python 02_run_core.py
python 03_check_result.py
```

각 파일을 실행한 뒤 값 하나를 바꾸고 결과 변화를 설명합니다.
""",
    )

    write(
        basic_dir / "basic_practice.py",
        f"""# {title} Basic Practice

{input_code}

print("=== 입력 확인 ===")
{show_code}

print("\\n=== 핵심 처리 ===")
{core_code}

print("\\n=== 결과 확인 ===")
{result_code}
""",
    )
    write(
        basic_dir / "README.md",
        f"""# {title} Basic Practice

Step by Step의 세 파일을 하나로 연결한 입문용 코드입니다.

```powershell
python basic_practice.py
```

완료 기준:

- 입력과 출력이 무엇인지 설명한다.
- 핵심 처리 부분을 코드에서 찾는다.
- 값 하나를 바꾸고 결과 차이를 설명한다.

도전: {challenge}
""",
    )

    write(
        starter_dir / "starter.py",
        f"""# {title} Practice Starter

{input_code}

print("입력을 먼저 확인하세요.")
{show_code}

# TODO 1: Basic Practice를 참고해 핵심 처리를 작성하세요.
# TODO 2: 처리 결과를 출력하세요.
# TODO 3: 아래 도전 과제를 하나 수행하세요.
# {challenge}
""",
    )
    write(
        starter_dir / "README.md",
        f"""# {title} Practice Starter

`starter.py`는 입력 확인까지만 구현되어 있습니다.

1. 코드를 실행해 입력을 확인합니다.
2. Basic Practice를 보지 않고 핵심 처리를 작성합니다.
3. 막히면 Step by Step의 필요한 파일만 확인합니다.
4. 결과를 설명한 뒤 기존 solution과 비교합니다.

도전: {challenge}

함수화, 타입 힌트, 외부 모델·API, 복합 검증은 기본 완료 기준이 아닙니다.
""",
    )

    learning_path = chapter_dir / "LEARNING_PATH.md"
    text = learning_path.read_text(encoding="utf-8")
    marker = "## 실행 코드 위치"
    block = f"""## 실행 코드 위치

- [Step by Step](examples/01_step_by_step/README.md)
- [Basic Practice](examples/02_basic_practice/README.md)
- [Practice Starter](examples/03_practice_starter/README.md)

세 자료는 외부 모델이나 API 없이 핵심 흐름을 먼저 이해하도록 구성했습니다. 실제 라이브러리와 완성형 구조는 기존 solution에서 비교합니다.
"""
    if marker in text:
        before = text.split(marker, 1)[0].rstrip()
        after_match = text.split(marker, 1)[1]
        next_heading = after_match.find("\n## ")
        after = after_match[next_heading + 1 :] if next_heading >= 0 else ""
        text = f"{before}\n\n{block}\n{after}"
    else:
        insert_at = text.find("\n## 3.")
        text = text[:insert_at].rstrip() + "\n\n" + block + "\n" + text[insert_at + 1 :]
    learning_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"쉬운 코드 생성: {chapter_dir.name}")


def main() -> None:
    for config in CHAPTERS:
        build_chapter(config)


if __name__ == "__main__":
    main()
