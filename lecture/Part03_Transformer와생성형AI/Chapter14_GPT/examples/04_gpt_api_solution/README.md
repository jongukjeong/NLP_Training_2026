# GPT API 활용

PowerShell에서 키와 선택 모델을 환경변수로 설정합니다.

```powershell
$env:OPENAI_API_KEY="..."
$env:OPENAI_MODEL="gpt-5.6-luna"
python gpt_api_example.py
```

API 호출에는 사용량에 따른 비용이 발생할 수 있습니다. 키·응답 원문·개인정보를 Git에 커밋하지 않습니다. 결과는 `output/responses.jsonl`에 생성됩니다.
