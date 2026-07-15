# 실습: GPT API 활용

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

CSV의 고객 문의를 읽어 간결한 답변 초안을 생성하고 요청 설정과 결과를 JSONL로 저장합니다.

- [안내](examples/04_gpt_api_solution/README.md)
- [코드](examples/04_gpt_api_solution/gpt_api_example.py)
- [입력](examples/04_gpt_api_solution/questions.csv)

현재 공식 모델 안내의 비용 민감형 모델을 기본값으로 사용하지만 `OPENAI_MODEL` 환경변수로 교체할 수 있습니다.

## 실습 목표

CSV 질문을 API에 보내 구조화된 답을 받고, 성공·실패·토큰·지연을 파일로 저장합니다. API 키는 환경변수로만 관리합니다.

## 요청 함수

```python
import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask(question):
    started = time.perf_counter()
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "사용할-모델"),
        input=f"질문에 간결히 답하세요.\n질문: {question}",
    )
    return response.output_text, time.perf_counter() - started
```

모델 이름과 API 형식은 실습 시점 공식 문서를 확인합니다.

## 질문 CSV

```csv
id,question,expected_keyword
q01,배송 기간은?,영업일
q02,환불 절차는?,취소
```

정답 문장 전체 일치보다 필수 키워드·JSON schema·근거 포함처럼 평가 가능한 조건을 둡니다.

## 실패 처리

- 인증·잘못된 요청: 재시도하지 않고 설정 수정
- timeout·일시적 rate limit: 제한 횟수 backoff
- JSON 실패: 파싱 오류 기록 후 한 번 재요청
- 근거 없음: 답변 보류

## 결과 파일

```text
id,model,prompt_version,output,passed,latency,error
```

개인정보와 API 키가 결과 파일에 들어가지 않게 합니다.

## 프롬프트 비교

Zero-shot과 Few-shot을 같은 질문으로 비교합니다. 정확도·형식 준수율·평균 입력 토큰·P95를 함께 봅니다.

## 완료 기준

최소 20개 질문, 오류 사례, 재시도 한도, 결과 CSV, 비용 추정, Prompt 버전과 안전 점검을 제출합니다.
