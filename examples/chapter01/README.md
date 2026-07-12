# Chapter 1 Examples

Chapter 1에서 사용하는 실행 가능한 예제 코드입니다.

## 파일 목록

| 파일 | 내용 |
|---|---|
| `01_simple_tokenization.py` | 간단한 공백 기준 토큰화 |
| `02_rule_based_intent.py` | 규칙 기반 고객 문의 의도 분류 |
| `03_sqlite_keyword_search.py` | SQLite 문서 저장과 키워드 검색 |
| `faq_data.py` | FAQ 챗봇 데이터 |
| `04_faq_chatbot.py` | 규칙 기반 FAQ 챗봇 |

## 실행 방법

프로젝트 루트에서 실행합니다.

```bash
python examples/chapter01/01_simple_tokenization.py
python examples/chapter01/02_rule_based_intent.py
python examples/chapter01/03_sqlite_keyword_search.py
python examples/chapter01/04_faq_chatbot.py
```

## 학습 포인트

- 컴퓨터는 텍스트를 그대로 의미로 이해하지 않는다.
- 간단한 규칙 기반 방식은 이해하기 쉽지만 표현 변화에 약하다.
- SQLite의 키워드 검색은 단어 포함 여부를 확인하는 데 유용하다.
- RAG에서는 의미가 비슷한 문서를 찾기 위해 임베딩과 벡터 검색이 필요하다.
