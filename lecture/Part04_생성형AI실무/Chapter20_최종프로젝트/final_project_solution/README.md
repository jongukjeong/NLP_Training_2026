# 최종 프로젝트 완성 예제

## 빠른 실행

```powershell
python src\evaluate.py
python src\app.py "환불 신청 기간은 며칠인가요?"
python -m pytest -q
```

`OPENAI_API_KEY`가 없으면 검색된 정책을 답변으로 사용합니다. 선택적으로 설정하면 Responses API가 검색 근거 안에서 답변 초안을 생성합니다.

```powershell
$env:OPENAI_API_KEY="..."
$env:OPENAI_MODEL="gpt-5.6-luna"
python src\app.py "배송비는 얼마인가요?"
```

## 구조

```text
final_project_solution/
├── data/
│   ├── knowledge.csv
│   └── evaluation.csv
├── src/
│   ├── retriever.py
│   ├── evaluate.py
│   └── app.py
├── tests/
│   └── test_retriever.py
└── templates/
```

주의: 교육용 정책 데이터입니다. 실제 서비스 연결 전 인증·권한·최신 정책 검증이 필요합니다.
