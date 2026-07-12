# Chapter 15 통합 강의 원고

입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 15. Hugging Face

1. [Transformers·AutoTokenizer·AutoModel](01_Auto_Classes.md)
2. [Pipeline과 Fine-tuning](02_Pipeline_and_Fine_Tuning.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 모델 활용](04_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_HuggingFace_모델선택과_실행점검.md -->

# Chapter 15 Hugging Face 모델 선택과 실행 점검

## 모델 검색보다 과제 정의가 먼저다

“한국어 모델”만 검색하지 말고 분류, 임베딩, 생성, 토큰 분류 중 어떤 출력이 필요한지 정합니다. 같은 BERT 계열이라도 기본 모델과 분류 Fine-tuning 모델은 바로 사용할 수 있는 출력이 다릅니다.

## 모델 카드에서 확인할 것

- 어떤 과제로 학습했는가?
- 지원 언어와 주요 학습 데이터는?
- 입력 최대 길이는?
- 라이선스와 사용 제한은?
- 알려진 편향과 한계는?
- 예제의 라이브러리 버전은?

다운로드 수가 많다는 이유만으로 업무 적합성을 보장하지 않습니다.

## Auto 클래스 선택

| 목적 | 대표 클래스 |
|---|---|
| 기본 표현 | AutoModel |
| 문장 분류 | AutoModelForSequenceClassification |
| 토큰 분류 | AutoModelForTokenClassification |
| GPT형 생성 | AutoModelForCausalLM |
| 번역·요약 | AutoModelForSeq2SeqLM |

잘못된 head를 선택하면 기대한 `logits` shape가 나오지 않습니다.

## Pipeline 결과 읽기

```python
result = classifier("배송이 늦어요")
print(result)
```

결과의 `label`이 `LABEL_0`이면 config의 `id2label`을 확인합니다. score는 모델의 예측 확률일 수 있지만 실제 신뢰도와 일치하는 calibration은 별도 평가가 필요합니다.

## CPU와 GPU

작은 모델·적은 요청은 CPU로도 충분할 수 있습니다. GPU는 batch 처리에서 장점이 크지만 데이터 전송과 메모리 제약이 있습니다. 한 문장 지연과 대량 throughput을 나눠 측정합니다.

## Dynamic padding

문장마다 항상 최대 길이까지 0을 붙이지 않고 같은 batch의 최장 문장까지만 padding하면 계산량을 줄일 수 있습니다. 길이가 비슷한 문장을 묶으면 더 효율적입니다.

## 메모리 부족 대응

batch 축소 → 최대 길이 축소 → gradient accumulation → mixed precision → 작은 모델 또는 양자화 순으로 영향과 품질을 측정합니다. 무조건 설정을 여러 개 동시에 바꾸지 않습니다.

## 저장과 재로딩 테스트

```python
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
```

새 프로세스에서 다시 불러와 대표 입력의 logits 또는 label이 같은지 확인합니다. 모델만 저장하고 tokenizer를 잃으면 동일 전처리를 재현할 수 없습니다.

## revision 고정

Hub의 같은 이름이 나중에 업데이트될 수 있습니다. 운영과 교육 재현을 위해 commit hash 또는 revision을 기록합니다. 라이브러리 버전도 requirements에 남깁니다.

## 실습 완료 기준

1. 모델 카드와 라이선스 확인
2. tokenizer/model checkpoint 일치
3. 입력과 logits shape 기록
4. label mapping 확인
5. CPU/GPU 지연 측정
6. 저장 후 재로딩 검증
7. 실제 한국어 오류 사례 분석

---

<!-- SOURCE: 00_HuggingFace_평가와_모델카드작성.md -->

# Chapter 15 Hugging Face 평가와 모델 카드 작성

## 우리 모델 카드

Fine-tuning 산출물에도 모델 카드를 작성합니다.

- 목적과 사용하지 말아야 할 용도
- 데이터 출처·기간·언어
- 레이블 정의
- 평가 지표와 하위집단 결과
- 알려진 실패와 편향
- 환경·라이브러리 버전
- 라이선스와 담당자

## 데이터 카드

샘플 수만 적지 말고 중복 제거, 개인정보, 분할 방법, 클래스 분포, 길이 분포를 기록합니다.

## Checkpoint 선택

마지막 checkpoint가 아니라 validation metric 최고 checkpoint를 선택합니다. Test는 최종 한 번 평가하며 test 결과로 checkpoint를 고르지 않습니다.

## Pipeline 회귀시험

대표 한국어 입력, 빈 입력, 매우 긴 입력, 이모지, 혼합 언어를 저장 후 재로딩 모델에 실행합니다. Label과 score 구조가 유지되는지 검사합니다.

## Hub 업로드 전 점검

가중치나 tokenizer에 개인정보가 직접 파일로 포함되지는 않았는지, README와 config에 비밀값이 없는지, 공개 범위와 라이선스를 확인합니다.

## 성능 보고

평균 F1 외에 클래스별 지표, 오류 문장, batch별 지연, peak memory를 포함합니다. 서로 다른 하드웨어 속도는 환경을 함께 씁니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 15 원리·수학·실습 가이드

## 1. 구성 요소 지도

Tokenizer는 문자열을 ID와 mask로 바꾸고, Model은 텐서를 로짓·임베딩으로 변환하며, Pipeline은 전처리부터 후처리까지 묶는다. Auto 클래스는 checkpoint 설정을 읽어 알맞은 구현 클래스를 선택한다.

`text → input_ids [B,T], attention_mask [B,T] → model → logits [B,C]`

## 2. Tokenizer 결과 읽기

```python
encoded = tokenizer(texts, padding=True, truncation=True,
                    max_length=128, return_tensors="pt")
for key, value in encoded.items():
    print(key, value.shape)
```

padding은 배치 길이를 맞추고, truncation은 최대 길이를 넘는 부분을 자른다. 잘린 문장 비율을 측정하지 않으면 중요한 결론이 사라진 것을 모르고 학습할 수 있다.

## 3. 로짓과 확률

모델 출력 로짓은 확률이 아니다. 다중 분류 확률은 Softmax로 바꾼다.

\[
p_i=\frac{e^{z_i}}{\sum_je^{z_j}}
\]

```python
with torch.no_grad():
    logits = model(**encoded).logits
probs = logits.softmax(dim=-1)
```

추론에서는 `eval()`과 `no_grad()`로 Dropout과 gradient 저장을 끈다.

## 4. Pipeline과 Fine-tuning

Pipeline은 빠른 검증에 좋지만 배치, 장치, label mapping을 명시적으로 확인한다. Fine-tuning 전에는 원본 데이터 스키마, 레이블 ID, train/valid 분할, seed를 고정한다. 학습 후 모델뿐 아니라 tokenizer, config, label mapping을 함께 저장한다.

모델 카드는 학습 데이터, 라이선스, 언어, 제한을 확인하는 출발점이다. 운영에서는 revision 고정, 원격 코드 실행 여부 검토, 입력 개인정보 제거가 필요하다.

1. `attention_mask=0`은 일반적으로 무엇을 뜻하는가?
2. 로짓을 확률로 바꾸는 함수는?
3. 모델과 함께 tokenizer를 저장해야 하는 이유는?

---

<!-- SOURCE: 01_Auto_Classes.md -->

# 15.1 Transformers · 15.2 AutoTokenizer · 15.3 AutoModel

Transformers는 다양한 architecture를 공통 인터페이스로 제공합니다. Auto Classes는 checkpoint의 config를 보고 알맞은 tokenizer/model class를 선택합니다.

```python
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
model = AutoModel.from_pretrained(model_id, revision=revision)
```

`AutoModel`은 task head 없는 backbone, `AutoModelForSequenceClassification` 등은 task head가 포함된 class입니다. config만 생성하는 것과 `from_pretrained()`로 weight를 내려받는 것을 구분합니다.

기록할 항목:

- repository model ID와 revision/commit
- tokenizer ID와 fast tokenizer 여부
- library·PyTorch 버전
- dtype, device, max_length
- license와 model card의 제한

`trust_remote_code=True`는 원격 코드를 실행할 수 있으므로 출처 검토 없이 활성화하지 않습니다.

## Auto 클래스가 해결하는 문제

Checkpoint마다 BERT, RoBERTa, GPT 등 구현 클래스가 다릅니다. `AutoConfig`가 설정을 읽고, `AutoTokenizer`와 `AutoModel`이 알맞은 클래스를 선택합니다. Auto가 모델 종류를 바꾸는 것이 아니라 저장소 설정에 맞춰 올바른 구현을 연결합니다.

## Tokenizer 출력 해석

```python
batch = tokenizer(
    ["첫 문장", "조금 더 긴 두 번째 문장"],
    padding=True,
    truncation=True,
    max_length=16,
    return_tensors="pt",
)
print(batch["input_ids"].shape)       # (2, T)
print(batch["attention_mask"].shape)  # (2, T)
```

`input_ids`는 토큰 번호, `attention_mask`의 1은 실제 토큰, 0은 패딩입니다. `token_type_ids`는 모델에 따라 없을 수 있습니다.

## AutoModel과 Task Head

`AutoModel`은 기본 hidden state를 반환합니다. 분류하려면 `AutoModelForSequenceClassification`, 토큰 분류는 `AutoModelForTokenClassification`, 생성은 CausalLM 또는 Seq2SeqLM용 클래스를 사용합니다. 작업 헤드가 다르면 출력 shape와 loss도 달라집니다.

## 로짓 확인

3분류 모델에 batch 8개를 넣으면 로짓은 `(8,3)`입니다. Softmax 뒤 각 행의 합은 1입니다. 모델 config의 `id2label`이 실제 데이터 레이블과 같은지 반드시 확인합니다.

## 안전한 모델 로딩

모델 카드에서 라이선스, 언어, 학습 데이터, 제한을 읽습니다. 운영 재현성을 위해 revision을 고정하고 원격 사용자 코드 실행 옵션은 출처를 검토한 뒤 사용합니다. tokenizer와 model은 같은 checkpoint에서 불러옵니다.

---

<!-- SOURCE: 02_Pipeline_and_Fine_Tuning.md -->

# 15.4 Pipeline · 15.5 Fine-tuning

Pipeline은 tokenizer, model 전처리와 후처리를 task별 API로 묶어 빠른 inference 기준선을 만듭니다.

```python
classifier = pipeline("text-classification", model=model_id)
classifier(["좋아요", "아쉬워요"])
```

명시적인 제어가 필요하면 tokenizer와 model을 직접 호출합니다. batching이 항상 빠른 것은 아니므로 sequence 길이와 device에서 측정합니다.

Fine-tuning 절차:

1. train/validation/test 분리
2. tokenizer로 truncation과 padding
3. task-specific AutoModel 로드
4. TrainingArguments와 Trainer 또는 직접 loop
5. metric과 checkpoint 선택
6. 모델·tokenizer·label mapping 저장

Hub에 push하기 전에 데이터·weight 라이선스, 개인정보와 공개 범위를 확인합니다.

## Pipeline을 자동 조리 기계로 비유하기

Pipeline은 재료 손질(tokenizer), 조리(model), 접시에 담기(post-processing)를 한 번에 수행합니다. 빠르게 모델을 시험하기 좋지만 내부 기본값을 모르면 최대 길이, 장치, label 의미를 잘못 해석할 수 있습니다.

```python
from transformers import pipeline
classifier = pipeline(
    "text-classification",
    model="사용할-checkpoint",
    device=-1,
)
print(classifier("배송이 너무 늦어요"))
```

`device=-1`은 일반적으로 CPU, GPU는 환경에 맞는 장치 번호를 지정합니다. 모델 카드의 label mapping을 확인하지 않고 `LABEL_0`을 긍정으로 가정하지 않습니다.

## Batch 추론

한 문장씩 반복 호출하는 것보다 리스트 또는 Dataset으로 batch 처리하면 장치를 효율적으로 사용할 수 있습니다. batch를 너무 크게 하면 메모리 부족이 생기므로 길이 분포와 GPU 메모리로 정합니다.

## Fine-tuning 데이터 흐름

```text
원본 데이터
 → tokenize(map)
 → train/validation Dataset
 → Data Collator로 batch padding
 → Model forward/loss
 → optimizer update
 → validation metric
```

Dynamic padding은 배치 안의 가장 긴 문장까지만 맞춰 고정 최대 길이 padding보다 계산을 줄일 수 있습니다.

## Data Collator의 역할

Tokenizer 결과를 같은 길이의 텐서 batch로 묶습니다. 토큰 분류에서는 subword와 원래 레이블 정렬이 필요하고, 언어모델 학습에서는 causal 또는 MLM용 레이블을 구성합니다. 과제마다 collator가 다릅니다.

## Trainer가 대신하는 것

Trainer는 학습 루프, evaluation, checkpoint, logging을 묶습니다. 데이터와 metric 정의를 대신 판단해 주는 것은 아닙니다. `TrainingArguments`의 evaluation/save 전략, batch, epoch, learning rate를 명시하고 버전에 따른 이름 변화를 확인합니다.

## metric 함수 주의

로짓에서 `argmax`로 예측 클래스를 만들고 정답과 비교합니다. padding label `-100`을 제외해야 하는 토큰 분류에서는 마스크 처리가 필요합니다. Accuracy 하나만 반환하지 말고 문제에 맞는 F1을 추가합니다.

## 저장 산출물

모델 가중치, config, tokenizer 파일, label mapping, 학습 파라미터, 평가 결과를 함께 저장합니다. 새 환경에서 `from_pretrained()`로 불러와 대표 입력의 결과를 비교합니다.

## 실무 점검

- 모델 라이선스와 상업적 사용 조건
- 입력 언어와 학습 언어 일치 여부
- 원격 코드 실행 옵션
- 개인정보가 외부 Hub로 업로드되지 않는지
- revision과 라이브러리 버전 고정

---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. Auto Classes의 역할은? **checkpoint config에 맞는 class 선택**
2. AutoModel과 AutoModelForSequenceClassification 차이는? **task head 유무**
3. `from_config`가 pretrained weight도 로드하나요? **아니요**
4. Pipeline의 장점은? **task별 전·후처리와 inference 간소화**
5. model과 tokenizer ID를 맞춰야 하나요? **예**
6. `trust_remote_code=True`의 위험은? **원격 코드 실행**
7. Hub 공개 전 확인할 것은? **라이선스·개인정보·공개 범위**

---

<!-- SOURCE: 04_Practice.md -->

# 실습: 한국어 모델 활용

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
