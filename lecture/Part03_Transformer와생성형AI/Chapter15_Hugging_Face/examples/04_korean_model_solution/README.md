# Hugging Face 한국어 모델 활용

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 공개 시점과 사용 방법

이 자료는 수강생이 기본 실습을 먼저 시도하고 피드백을 받은 뒤 공개하는 완성형 참고 자료입니다. 기본 코드보다 복잡한 것이 정상이며, 전체를 복사하기보다 자신의 코드와 구조·검증·오류 처리 방식을 비교합니다.
<!-- END: BEGINNER_LEARNING_PATH -->

```powershell
python huggingface_korean_model.py
```

기본값은 `klue/bert-base`이며 `HF_MODEL_ID`로 다른 fill-mask 호환 모델을 지정할 수 있습니다. 첫 실행에는 Hub 다운로드가 필요합니다. 결과는 `output/predictions.json`에 저장됩니다.
