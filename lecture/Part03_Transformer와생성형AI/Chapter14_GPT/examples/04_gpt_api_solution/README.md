# GPT API 활용

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 공개 시점과 사용 방법

이 자료는 수강생이 기본 실습을 먼저 시도하고 피드백을 받은 뒤 공개하는 완성형 참고 자료입니다. 기본 코드보다 복잡한 것이 정상이며, 전체를 복사하기보다 자신의 코드와 구조·검증·오류 처리 방식을 비교합니다.
<!-- END: BEGINNER_LEARNING_PATH -->

PowerShell에서 키와 선택 모델을 환경변수로 설정합니다.

```powershell
$env:OPENAI_API_KEY="..."
$env:OPENAI_MODEL="gpt-5.6-luna"
python gpt_api_example.py
```

API 호출에는 사용량에 따른 비용이 발생할 수 있습니다. 키·응답 원문·개인정보를 Git에 커밋하지 않습니다. 결과는 `output/responses.jsonl`에 생성됩니다.
