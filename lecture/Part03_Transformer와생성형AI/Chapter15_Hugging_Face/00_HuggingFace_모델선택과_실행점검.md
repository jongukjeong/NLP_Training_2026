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
