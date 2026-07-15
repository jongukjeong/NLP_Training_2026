# 실습: 한국어 모델 활용

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

한국어 BERT의 fill-mask pipeline과 AutoTokenizer/AutoModel 정보를 함께 확인합니다.

- [안내](examples/04_korean_model_solution/README.md)
- [코드](examples/04_korean_model_solution/huggingface_korean_model.py)
- [입력](examples/04_korean_model_solution/prompts.csv)

## 실습 목표

한국어 checkpoint를 선택하고 tokenizer·model·pipeline 결과를 비교한 뒤, 저장과 재로딩까지 검증합니다.

## 모델 선택 기록

```text
checkpoint:
task:
language:
license:
max length:
revision:
known limitations:
```

다운로드 수만 보고 선택하지 않고 모델 카드와 업무 평가셋을 확인합니다.

## Tokenizer 검사

```python
encoded = tokenizer(
    ["배송이 늦어요", "환불을 요청합니다"],
    padding=True,
    truncation=True,
    return_tensors="pt",
)
for key, value in encoded.items():
    print(key, value.shape)
```

토큰 문자열, ID, attention mask를 함께 출력합니다.

## 직접 추론과 Pipeline

```python
model.eval()
with torch.no_grad():
    logits = model(**encoded).logits
probs = logits.softmax(dim=-1)
```

Pipeline 결과의 label·score와 직접 계산 결과가 같은 의미인지 `id2label`로 확인합니다.

## Batch 성능

Batch 1·8·32에서 샘플당 지연과 peak memory를 측정합니다. GPU는 동기화와 warm-up 조건을 기록합니다.

## 저장 검증

```python
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
```

새 프로세스에서 불러와 고정 입력 logits가 허용 오차 안에서 같은지 비교합니다.

## 오류 사례

긴 문장 truncation, 혼합 언어, 이모지, 빈 입력, label mapping 불일치, revision 변경을 테스트합니다.

## 완료 기준

모델 카드 선택 근거, 입력·출력 shape, 평가 지표, 속도, 오류 문장, 저장·재로딩 테스트와 라이선스를 제출합니다.
