# 로컬 LLM 실행

Ollama 설치 후 모델을 준비합니다.

```powershell
ollama pull gemma3:1b
$env:OLLAMA_MODEL="gemma3:1b"
python local_llm_runner.py
```

모델 tag는 환경에 맞게 바꿉니다. 응답과 사용량 metadata는 `output/responses.jsonl`에 저장됩니다.
