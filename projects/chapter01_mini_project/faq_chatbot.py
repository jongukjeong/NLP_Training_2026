"""키워드 점수로 문의 유형을 분류하는 Chapter 1 미니 프로젝트."""

from faq_data import FALLBACK_RESPONSE, FAQ_DATA


def calculate_scores(text: str) -> dict[str, int]:
    """카테고리별로 포함된 키워드 수를 계산한다."""
    normalized = text.strip().lower()
    return {
        category: sum(keyword.lower() in normalized for keyword in item["keywords"])
        for category, item in FAQ_DATA.items()
    }


def classify_intent(text: str) -> tuple[str | None, dict[str, int]]:
    """가장 높은 점수의 카테고리를 반환하며 동점은 데이터 선언 순서를 따른다."""
    scores = calculate_scores(text)
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return None, scores
    return best_category, scores


def get_response(text: str) -> tuple[str | None, str, dict[str, int]]:
    category, scores = classify_intent(text)
    response = FALLBACK_RESPONSE if category is None else FAQ_DATA[category]["response"]
    return category, response, scores


def run_chatbot() -> None:
    print("Chapter 1 FAQ 챗봇입니다. 종료하려면 q를 입력하세요.")
    while True:
        user_input = input("질문: ").strip()
        if user_input.lower() in {"q", "quit", "exit"}:
            print("챗봇을 종료합니다.")
            break
        if not user_input:
            print("질문을 입력해 주세요.")
            continue
        category, response, scores = get_response(user_input)
        print("분류:", category or "기타 문의")
        print("점수:", scores)
        print("답변:", response)


if __name__ == "__main__":
    run_chatbot()
