# Chapter 15. Hugging Face — 통합 원고

> 이 문서는 Chapter 15. Hugging Face 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 15. Hugging Face — `README.md`
- 15.1 Transformers · 15.2 AutoTokenizer · 15.3 AutoModel — `01_Auto_Classes.md`
- 15.4 Pipeline · 15.5 Fine-tuning — `02_Pipeline_and_Fine_Tuning.md`
- 요약과 퀴즈 — `03_Summary_and_Quiz.md`
- 실습: 한국어 모델 활용 — `04_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 15. Hugging Face

# Chapter 15. Hugging Face

1. [Transformers·AutoTokenizer·AutoModel](01_Auto_Classes.md)
2. [Pipeline과 Fine-tuning](02_Pipeline_and_Fine_Tuning.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 모델 활용](04_Practice.md)


---

<!-- SOURCE: 01_Auto_Classes.md -->

# 15.1 Transformers · 15.2 AutoTokenizer · 15.3 AutoModel

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


---

<!-- SOURCE: 02_Pipeline_and_Fine_Tuning.md -->

# 15.4 Pipeline · 15.5 Fine-tuning

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

# 실습: 한국어 모델 활용

한국어 BERT의 fill-mask pipeline과 AutoTokenizer/AutoModel 정보를 함께 확인합니다.

- [안내](examples/04_korean_model_solution/README.md)
- [코드](examples/04_korean_model_solution/huggingface_korean_model.py)
- [입력](examples/04_korean_model_solution/prompts.csv)

