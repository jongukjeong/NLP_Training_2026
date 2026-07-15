# 로컬 LLM 실행

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 공개 시점과 사용 방법

이 자료는 수강생이 기본 실습을 먼저 시도하고 피드백을 받은 뒤 공개하는 완성형 참고 자료입니다. 기본 코드보다 복잡한 것이 정상이며, 전체를 복사하기보다 자신의 코드와 구조·검증·오류 처리 방식을 비교합니다.
<!-- END: BEGINNER_LEARNING_PATH -->

Ollama 설치 후 모델을 준비합니다.

```powershell
ollama pull gemma3:1b
$env:OLLAMA_MODEL="gemma3:1b"
python local_llm_runner.py
```

모델 tag는 환경에 맞게 바꿉니다. 응답과 사용량 metadata는 `output/responses.jsonl`에 저장됩니다.
