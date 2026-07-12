# 실습: 로컬 LLM 실행

- [안내](examples/04_local_llm_solution/README.md)
- [코드](examples/04_local_llm_solution/local_llm_runner.py)
- [입력](examples/04_local_llm_solution/prompts.csv)

Ollama 모델명을 환경변수로 받아 응답과 성능 metadata를 JSONL로 기록합니다.

## 실습 준비

로컬 런타임과 모델을 선택하기 전에 장비 정보를 기록합니다.

```text
OS:
CPU/RAM:
GPU/VRAM:
Runtime 버전:
모델 태그·양자화:
```

모델 파일 크기와 실제 peak memory는 다르므로 실행 중 값을 측정합니다.

## 고정 Prompt 세트

요약, 분류, 한국어 질의응답, 구조화 출력, 긴 문맥 질문을 최소 20개 준비합니다. 모델마다 같은 입력과 최대 출력 길이, temperature를 사용합니다.

## 측정 코드의 핵심

```python
started = time.perf_counter()
result = generate(prompt)
elapsed = time.perf_counter() - started
```

가능하면 첫 토큰 시간과 전체 시간을 분리합니다. 첫 실행은 모델 로딩을 포함하므로 cold와 warm 실행을 나눕니다.

## 결과 CSV

```text
model,quantization,prompt_id,passed,ttft,total_seconds,tokens_per_second,error
```

정답성은 필수 키워드, JSON schema, 사람 평가 기준으로 판정합니다.

## 동시성 실험

동시 요청 1·2·4개에서 P50/P95와 오류율을 비교합니다. 한 요청이 빠른 것과 여러 사용자를 안정적으로 처리하는 것은 다릅니다.

## 안전 점검

모델 서버가 외부 인터페이스에 인증 없이 열리지 않았는지 확인하고 Prompt 로그의 개인정보를 마스킹합니다. 모델 라이선스와 출처도 기록합니다.

## 완료 기준

두 개 이상 모델 또는 양자화 설정, 20개 이상 질문, 품질·TTFT·tokens/s·메모리 표, 실패 사례와 선택 결론을 제출합니다.
