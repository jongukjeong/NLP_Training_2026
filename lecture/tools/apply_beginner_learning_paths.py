from pathlib import Path
import re


LECTURE_DIR = Path(__file__).resolve().parent.parent
START = "<!-- BEGIN: BEGINNER_LEARNING_PATH -->"
END = "<!-- END: BEGINNER_LEARNING_PATH -->"


CHAPTERS = [
    ("Part01_자연어처리기초와Python/Chapter01_인공지능과자연어처리의이해", "Chapter 1", "NLP 문제와 규칙 기반 분류의 흐름 이해", ["문장과 토큰을 출력한다", "키워드 한 개로 의도를 구분한다", "여러 질문으로 규칙을 시험한다", "FAQ 챗봇 기본 기능을 완성한다"], "11_Mini_Project.md", "projects/README.md", ["SQLite 검색", "테스트 자동화", "LLM·RAG 확장"]),
    ("Part01_자연어처리기초와Python/Chapter03_텍스트전처리", "Chapter 3", "한 문장씩 공백과 표기를 정리하고 전후를 비교", ["원문과 정제문을 나란히 출력한다", "공백 한 가지 규칙만 적용한다", "URL·이메일 규칙을 하나씩 추가한다", "여러 문장의 처리 통계를 확인한다"], "09_Mini_Project.md", "examples/09_mini_project_solution/README.md", ["함수 분리", "정규표현식 조합", "형태소 분석", "품질 보고서"]),
    ("Part01_자연어처리기초와Python/Chapter04_텍스트의수치화", "Chapter 4", "작은 문서 세 개를 숫자로 바꾸고 검색 결과 확인", ["단어 목록을 직접 센다", "BoW 행렬의 한 행을 읽는다", "TF-IDF 점수를 비교한다", "질문 하나로 가장 가까운 문서를 찾는다"], "08_Mini_Project.md", "examples/08_mini_project_solution/README.md", ["n-gram", "평가 데이터", "검색 지표", "실험 보고서"]),
    ("Part01_자연어처리기초와Python/Chapter05_단어임베딩", "Chapter 5", "작은 단어 집합에서 유사도와 이웃 단어 확인", ["단어를 벡터로 표현한다", "두 벡터의 유사도를 비교한다", "가장 가까운 단어를 찾는다", "결과가 의미에 맞는지 설명한다"], "08_Mini_Project.md", "examples/08_mini_project_solution/README.md", ["동시출현 행렬", "SVD", "사전학습 임베딩", "편향 평가"]),
    ("Part02_딥러닝기반자연어처리/Chapter06_TensorFlow와Keras", "Chapter 6", "Tensor의 shape를 확인하고 작은 Keras 모델 실행", ["Tensor를 만들고 shape를 출력한다", "Dataset에서 배치 하나를 확인한다", "층 하나의 모델을 만든다", "한 번 학습하고 예측값을 본다"], "05_Practice.md", "examples/05_first_model_solution/README.md", ["콜백", "재현성 설정", "성능 개선", "저장·복원"]),
    ("Part02_딥러닝기반자연어처리/Chapter07_딥러닝기초", "Chapter 7", "작은 텍스트 분류 모델의 입력·출력과 손실 확인", ["입력과 레이블을 확인한다", "모델 층별 shape를 읽는다", "한 epoch 학습한다", "예측과 정답을 비교한다"], "05_Practice.md", "examples/05_text_classification_solution/README.md", ["최적화 비교", "과적합 진단", "하이퍼파라미터", "오류 분석"]),
    ("Part02_딥러닝기반자연어처리/Chapter08_순환신경망_RNN", "Chapter 8", "짧은 문장이 RNN을 통과하는 shape 흐름 확인", ["토큰 시퀀스를 확인한다", "배치·길이·차원 축을 구분한다", "RNN 출력 shape를 확인한다", "문장 분류 결과를 비교한다"], "05_Practice.md", "examples/05_sentence_classification_solution/README.md", ["BPTT", "padding·mask", "모델 비교", "디버깅"]),
    ("Part02_딥러닝기반자연어처리/Chapter09_LSTM과GRU", "Chapter 9", "같은 문장을 LSTM과 GRU로 실행해 결과 비교", ["입력 시퀀스를 확인한다", "LSTM 출력 shape를 본다", "GRU 출력 shape를 본다", "두 모델의 예측과 학습 시간을 비교한다"], "05_Practice.md", "examples/05_sentiment_solution/README.md", ["게이트 계산", "양방향 모델", "모델 선택", "세부 평가"]),
    ("Part02_딥러닝기반자연어처리/Chapter10_Seq2Seq와Encoder_Decoder", "Chapter 10", "짧은 입력·정답 문장의 Encoder-Decoder 흐름 확인", ["입력과 목표 시퀀스를 확인한다", "Encoder 상태 shape를 본다", "Decoder의 한 단계 출력을 본다", "짧은 번역 결과를 정답과 비교한다"], "06_Practice.md", "examples/06_translation_solution/README.md", ["teacher forcing", "beam search", "BLEU", "오류 분석"]),
    ("Part03_Transformer와생성형AI/Chapter11_Attention_Mechanism", "Chapter 11", "작은 Attention 행렬에서 한 행의 의미 설명", ["토큰 세 개를 준비한다", "유사도 점수를 확인한다", "softmax 합이 1인지 확인한다", "가중합 결과를 해석한다"], "03_Practice.md", "examples/03_attention_visualization_solution/README.md", ["행렬 계산", "시각화", "mask", "오류 진단"]),
    ("Part03_Transformer와생성형AI/Chapter12_Transformer", "Chapter 12", "Transformer 블록의 입력과 출력 shape 추적", ["토큰·위치 표현을 확인한다", "Attention 입출력 shape를 본다", "잔차 연결 전후를 비교한다", "Encoder 블록 한 개를 실행한다"], "04_Practice.md", "examples/04_transformer_solution/README.md", ["직접 구현", "mask 테스트", "성능·메모리", "작은 데이터 과적합"]),
    ("Part03_Transformer와생성형AI/Chapter13_BERT", "Chapter 13", "한국어 문장을 토큰화하고 BERT 표현 shape 확인", ["문장 두 개를 준비한다", "Tokenizer 출력을 읽는다", "모델 출력 shape를 확인한다", "두 문장의 표현을 비교한다"], "04_Practice.md", "examples/04_korean_bert_solution/README.md", ["fine-tuning", "평가 함수", "오류 분석", "배포 점검"]),
    ("Part03_Transformer와생성형AI/Chapter14_GPT", "Chapter 14", "같은 질문에 두 프롬프트를 적용하고 결과 비교", ["짧은 질문 하나를 정한다", "기본 프롬프트 결과를 기록한다", "조건을 한 가지 추가한다", "두 결과를 기준표로 비교한다"], "04_Practice.md", "examples/04_gpt_api_solution/README.md", ["API 재시도", "회귀 시험", "비용 기록", "안전 필터"]),
    ("Part03_Transformer와생성형AI/Chapter15_Hugging_Face", "Chapter 15", "Pipeline으로 모델 하나를 실행하고 입출력 확인", ["모델 카드를 확인한다", "Tokenizer 결과를 출력한다", "Pipeline으로 문장 하나를 실행한다", "여러 문장의 결과를 비교한다"], "04_Practice.md", "examples/04_korean_model_solution/README.md", ["직접 추론", "batch 성능", "모델 저장", "모델 카드 작성"]),
    ("Part04_생성형AI실무/Chapter16_대규모언어모델_LLM", "Chapter 16", "고정 프롬프트로 로컬 LLM 응답과 실행 시간 기록", ["실행 가능한 모델을 선택한다", "프롬프트 하나를 입력한다", "응답과 시간을 기록한다", "두 설정의 결과를 비교한다"], "04_Practice.md", "examples/04_local_llm_solution/README.md", ["동시성", "용량 계획", "벤치마크", "안전 점검"]),
    ("Part04_생성형AI실무/Chapter17_Prompt_Engineering", "Chapter 17", "프롬프트 한 요소씩 바꾸며 결과 품질 비교", ["평가 질문을 고정한다", "기본 프롬프트를 실행한다", "역할 또는 형식을 하나 추가한다", "간단한 기준표로 결과를 비교한다"], "05_Practice.md", "examples/05_prompt_optimization_solution/README.md", ["버전 관리", "자동 평가", "회귀 시험", "운영 모니터링"]),
    ("Part04_생성형AI실무/Chapter18_RAG", "Chapter 18", "작은 문서에서 검색 결과와 근거 문장 확인", ["문서 세 개를 준비한다", "질문과 가까운 문서를 찾는다", "검색된 근거를 출력한다", "답변이 근거에 포함되는지 확인한다"], "05_Practice.md", "examples/05_pdf_qa_solution/README.md", ["PDF loader", "chunk 실험", "hybrid 검색", "RAG 평가"]),
    ("Part04_생성형AI실무/Chapter19_AI_Agent와최신프레임워크", "Chapter 19", "도구 하나를 가진 단순 Agent의 선택과 결과 확인", ["도구의 입력과 출력을 정한다", "질문 하나에 도구를 선택한다", "도구 결과를 응답에 반영한다", "실패 질문에서 안전하게 중단한다"], "05_Practice.md", "examples/05_ai_assistant_solution/README.md", ["MCP", "다중 도구", "실패 복구", "운영 평가"]),
    ("Part04_생성형AI실무/Chapter20_최종프로젝트", "Chapter 20", "작은 근거 기반 고객지원 흐름을 끝까지 완성", ["사용자와 문제를 한 문장으로 정의한다", "지식 문서 세 개를 준비한다", "질문 하나의 검색·답변 흐름을 만든다", "테스트 사례로 결과를 확인한다"], "00_최종프로젝트_단계별_워크북.md", "final_project_solution/README.md", ["서비스 UI", "자동 평가", "보안·권한", "배포·모니터링"]),
]


def replace_or_insert(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    wrapped = f"{START}\n{block.strip()}\n{END}"
    if START in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), wrapped, text, flags=re.S)
    else:
        first_line, rest = text.split("\n", 1)
        text = f"{first_line}\n\n{wrapped}\n\n{rest.lstrip()}"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def learning_path(chapter: str, goal: str, steps: list[str], advanced: list[str], task: str, solution: str) -> str:
    step_lines = "\n".join(f"{i}. {step}" for i, step in enumerate(steps, 1))
    advanced_lines = "\n".join(f"- {item}" for item in advanced)
    return f"""# {chapter} 비전공자 학습 경로

## 기본 도달 목표

{goal}

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

{step_lines}

각 단계가 끝날 때 입력, 출력 또는 중간 결과를 화면에서 확인합니다. 설명할 수 없는 줄은 다음 단계로 넘어가기 전에 질문합니다.

## 2. Basic Practice — 짧은 흐름 연결

Step by Step의 네 단계를 한 흐름으로 연결합니다. 처음에는 함수 분리, 타입 힌트, 복잡한 예외 처리와 자동 보고서를 요구하지 않습니다.

완료 확인:

- 입력이 무엇인지 설명한다.
- 핵심 처리 한 단계를 찾아 수정한다.
- 출력이 예상과 다른 이유를 한 가지 찾는다.
- 실행 결과를 짧게 기록한다.

## 3. Practice·Assignment — 먼저 시도

[{task}]({task})의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[{solution}]({solution})은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

{advanced_lines}

선택 확장은 기본 완료 기준에 포함하지 않습니다.
"""


def rebuild_complete(chapter_dir: Path) -> None:
    complete_files = list(chapter_dir.glob("Chapter*_Complete.md"))
    if not complete_files:
        return
    output = complete_files[0]
    old = output.read_text(encoding="utf-8")
    sources = re.findall(r"<!-- SOURCE: ([^>]+) -->", old)
    if not sources:
        return
    title = old.split("\n", 1)[0].rstrip()
    ordered = []
    for source in sources:
        if source == "README.md":
            ordered.extend(["README.md", "LEARNING_PATH.md"])
        elif source == "LEARNING_PATH.md":
            continue
        else:
            ordered.append(source)
    sections = [title]
    for source in ordered:
        path = chapter_dir / source
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8").strip()
        content = "\n".join(line.rstrip() for line in raw.splitlines())
        sections.append(f"<!-- SOURCE: {source} -->\n\n{content}")
    output.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    for relative, chapter, goal, steps, task, solution, advanced in CHAPTERS:
        chapter_dir = LECTURE_DIR / relative
        content = learning_path(chapter, goal, steps, advanced, task, solution)
        (chapter_dir / "LEARNING_PATH.md").write_text(content, encoding="utf-8")

        readme_block = f"""## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다."""
        replace_or_insert(chapter_dir / "README.md", readme_block)

        task_path = chapter_dir / task
        task_block = f"""## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다."""
        replace_or_insert(task_path, task_block)

        solution_path = chapter_dir / solution
        solution_block = """## 공개 시점과 사용 방법

이 자료는 수강생이 기본 실습을 먼저 시도하고 피드백을 받은 뒤 공개하는 완성형 참고 자료입니다. 기본 코드보다 복잡한 것이 정상이며, 전체를 복사하기보다 자신의 코드와 구조·검증·오류 처리 방식을 비교합니다."""
        replace_or_insert(solution_path, solution_block)
        rebuild_complete(chapter_dir)
        print(f"적용 완료: {chapter_dir.name}")


if __name__ == "__main__":
    main()
