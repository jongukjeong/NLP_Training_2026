# Seq2Seq 번역 모델 완성 예제

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 공개 시점과 사용 방법

이 자료는 수강생이 기본 실습을 먼저 시도하고 피드백을 받은 뒤 공개하는 완성형 참고 자료입니다. 기본 코드보다 복잡한 것이 정상이며, 전체를 복사하기보다 자신의 코드와 구조·검증·오류 처리 방식을 비교합니다.
<!-- END: BEGINNER_LEARNING_PATH -->

```powershell
python seq2seq_translation.py
```

같은 폴더의 `translations.csv`로 문자 단위 Encoder-Decoder를 학습합니다. `output/`에 모델과 vocabulary 설정을 저장합니다. 교육용 데이터가 매우 작으므로 번역 품질 평가용이 아닙니다.
