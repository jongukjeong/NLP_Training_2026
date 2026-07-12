# 로컬 LLM 실행과 운영 판단

로컬 실행 장점은 데이터 경계와 실험 통제이며, 단점은 hardware·배포·보안 패치·모델 관리 책임입니다.

Ollama 기본 흐름:

```text
모델 pull → local API 실행 → prompt 요청 → token/latency 기록
```

정량 기록:

- prompt/output token 수
- load/prompt evaluation/generation 시간
- tokens per second
- peak memory
- model tag와 digest
- generation parameters

양자화는 memory를 줄일 수 있지만 품질과 속도 변화가 있으므로 동일 평가셋으로 비교합니다. 민감 데이터가 로컬이라는 이유만으로 안전한 것은 아니며 로그, cache, model access와 OS 권한을 관리해야 합니다.
