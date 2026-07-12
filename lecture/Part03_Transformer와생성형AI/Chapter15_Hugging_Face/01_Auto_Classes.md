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
