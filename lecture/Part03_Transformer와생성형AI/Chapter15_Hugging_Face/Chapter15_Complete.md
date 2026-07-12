# Chapter 15 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

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

