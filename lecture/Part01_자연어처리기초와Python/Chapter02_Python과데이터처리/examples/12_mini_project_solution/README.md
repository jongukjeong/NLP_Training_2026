# Chapter 2 미니 프로젝트 완성 예제

코드와 입력 데이터셋을 같은 폴더에 둔 강의 배포용 예제입니다. 수강생이 starter의 기본 요구사항을 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.

이 코드는 CLI, 함수, 타입 힌트, 오류 검사와 JSON 보고서를 포함한 **선택 확장 solution**입니다. 인수 없이 실행하면 함께 제공된 `reviews.csv`를 사용합니다.

```powershell
python text_data_explorer.py
```

다른 파일과 출력 경로를 지정할 수도 있습니다.

```powershell
python text_data_explorer.py reviews.csv output\reviews_clean.csv
```

생성 파일:

- `output/reviews_clean.csv`
- `output/reviews_clean.report.json`
