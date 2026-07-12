# 실습: PDF QA 시스템 구축

정책 원문으로 교육용 PDF를 생성하고, PDF text를 page별로 추출한 뒤 TF-IDF 검색과 출처 표시 QA를 수행합니다. API 키 없이 retrieval QA가 동작합니다.

- [안내](examples/05_pdf_qa_solution/README.md)
- [PDF 생성](examples/05_pdf_qa_solution/build_sample_pdf.py)
- [QA 코드](examples/05_pdf_qa_solution/pdf_qa.py)
- [정책 원문](examples/05_pdf_qa_solution/policy_source.txt)
- [평가셋](examples/05_pdf_qa_solution/evaluation.csv)

## PDF QA 구축 단계

1. PDF에서 텍스트와 page metadata 로드
2. 빈 페이지와 추출 오류 검사
3. 문단 또는 token 기준 chunk
4. Embedding 생성과 Vector Store 저장
5. 질문 검색과 top-k 출력
6. 문맥 기반 답변과 페이지 인용
7. 평가 CSV 실행

## Loader 검사

임의 페이지 5개를 원본 PDF와 비교합니다. 표·다단 편집·스캔 PDF는 읽기 순서나 OCR 오류가 발생할 수 있습니다.

## Chunk 실험표

| 크기/중첩 | Hit@3 | MRR | 근거성 | P95 |
|---|---:|---:|---:|---:|
| 300/50 | 기록 | 기록 | 기록 | 기록 |
| 600/100 | 기록 | 기록 | 기록 | 기록 |

## 검색 출력

질문마다 문서 ID, 페이지, score와 chunk 원문 일부를 저장합니다. 답변만 저장하면 검색 오류를 추적하기 어렵습니다.

## 권한과 보안

파일 경로를 사용자 입력과 직접 결합하지 않고 허용 디렉터리 안의 문서만 처리합니다. Prompt와 로그에서 개인정보를 마스킹합니다.

## 완료 기준

샘플 PDF, 구축 명령, 20개 이상 평가 질문, 검색·생성 분리 지표, 오류 사례, 재색인 방법과 인용 검증을 제출합니다.
