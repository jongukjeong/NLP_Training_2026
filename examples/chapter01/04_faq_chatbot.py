"""
Chapter 1 Example 04
규칙 기반 FAQ 챗봇 예제

실행:
    python examples/chapter01/04_faq_chatbot.py

종료:
    q 입력
"""

from faq_data import FAQ_RESPONSES, INTENT_KEYWORDS


def calculate_scores(text: str) -> dict[str, int]:
    """각 문의 유형별 키워드 매칭 점수를 계산합니다."""
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        scores[intent] = score
    return scores


def detect_intent(text: str) -> str:
    """가장 높은 점수를 가진 문의 유형을 반환합니다."""
    scores = calculate_scores(text)
    best_intent = max(scores, key=scores.get)
    if scores[best_intent] == 0:
        return "기타 문의"
    return best_intent


def get_response(text: str) -> tuple[str, str]:
    """사용자 문장에 대한 분류 결과와 응답 문장을 반환합니다."""
    intent = detect_intent(text)
    response = FAQ_RESPONSES[intent]
    return intent, response


def run_test_cases() -> None:
    """고정 테스트 문장을 실행합니다."""
    test_sentences = [
        "배송이 아직 안 왔어요.",
        "택배 운송장을 확인하고 싶어요.",
        "환불은 어떻게 하나요?",
        "상품을 돌려보내고 싶어요.",
        "카드 결제가 실패했습니다.",
        "영수증을 받을 수 있나요?",
        "비밀번호를 잊어버렸어요.",
        "로그인이 안 됩니다.",
        "이 제품 다른 색상 있나요?",
        "상품 재고가 있나요?",
        "상담원과 통화하고 싶어요.",
    ]
    for sentence in test_sentences:
        intent, response = get_response(sentence)
        print("질문:", sentence)
        print("분류:", intent)
        print("답변:", response)
        print("-" * 50)


def run_chatbot() -> None:
    """사용자 입력을 받아 FAQ 챗봇을 실행합니다."""
    print("FAQ 챗봇입니다.")
    print("종료하려면 q를 입력하세요.")
    print("-" * 50)
    while True:
        user_input = input("질문을 입력하세요: ")
        if user_input.lower() == "q":
            print("챗봇을 종료합니다.")
            break
        intent, response = get_response(user_input)
        print("분류:", intent)
        print("답변:", response)
        print("-" * 50)


if __name__ == "__main__":
    print("[테스트 케이스 실행]")
    run_test_cases()
    print()
    print("[대화형 챗봇 실행]")
    run_chatbot()
