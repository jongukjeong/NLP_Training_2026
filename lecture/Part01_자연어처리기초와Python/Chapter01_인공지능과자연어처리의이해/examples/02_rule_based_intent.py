"""
Chapter 1 Example 02
규칙 기반 고객 문의 의도 분류 예제

실행:
    python examples/chapter01/02_rule_based_intent.py
"""

def detect_intent(text: str) -> str:
    """문장 안에 포함된 키워드를 기준으로 문의 유형을 분류합니다."""
    if "환불" in text or "반품" in text or "취소" in text:
        return "환불 문의"
    if "배송" in text or "택배" in text or "도착" in text or "운송장" in text:
        return "배송 문의"
    if "결제" in text or "카드" in text or "입금" in text or "영수증" in text:
        return "결제 문의"
    if "비밀번호" in text or "로그인" in text or "계정" in text or "아이디" in text:
        return "계정 문의"
    if "상품" in text or "제품" in text or "재고" in text or "사이즈" in text:
        return "상품 문의"
    return "기타 문의"


def main() -> None:
    sentences = [
        "상품 환불은 어떻게 하나요?",
        "배송이 아직 안 왔어요.",
        "택배 운송장을 확인하고 싶어요.",
        "결제가 두 번 된 것 같아요.",
        "카드 승인이 실패했습니다.",
        "비밀번호를 잊어버렸어요.",
        "로그인이 안 됩니다.",
        "이 제품은 다른 색상이 있나요?",
        "상품 재고가 있나요?",
        "상담원과 통화하고 싶어요.",
    ]
    for sentence in sentences:
        print(f"{sentence} → {detect_intent(sentence)}")


if __name__ == "__main__":
    main()
