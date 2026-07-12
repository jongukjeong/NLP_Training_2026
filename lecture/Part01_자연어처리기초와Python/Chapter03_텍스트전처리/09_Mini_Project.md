# 09. 미니 프로젝트: 전처리 품질 리포터

## 목표

CSV의 텍스트를 전처리하고 결과뿐 아니라 **어떤 변화가 얼마나 발생했는지** JSON 보고서로 남기는 배포 가능한 프로그램을 완성합니다.

## 필수 기능

1. 입력·출력 경로를 명령행 인수로 선택하며 기본 경로를 제공합니다.
2. `id`, `text` 필수 열을 검사합니다.
3. Unicode NFC, 보이지 않는 문자, 연속 공백을 처리합니다.
4. URL·이메일·전화번호를 유형 토큰으로 마스킹합니다.
5. 원본과 정제 텍스트, 문자 수와 토큰 수를 함께 저장합니다.
6. 처리 행 수, 마스킹 수, 평균 길이 변화, 빈 결과 수를 보고합니다.
7. 입력 파일은 덮어쓰지 않습니다.

## 권장 구조

```text
examples/09_mini_project_solution/
├── preprocessing_reporter.py
├── messages.csv
└── output/                    # 실행 시 생성
```

## 실행

```powershell
cd lecture\Part01_자연어처리기초와Python\Chapter03_텍스트전처리\examples\09_mini_project_solution
python preprocessing_reporter.py
```

## 배포용 완성 예제

- [완성 예제 안내](examples/09_mini_project_solution/README.md)
- [완성 예제 코드](examples/09_mini_project_solution/preprocessing_reporter.py)
- [입력 데이터셋](examples/09_mini_project_solution/messages.csv)
