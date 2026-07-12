"""외부 테스트 프레임워크 없이 실행할 수 있는 간단한 검증 스크립트."""

from faq_chatbot import classify_intent


TEST_CASES = [
    ("배송이 아직 도착하지 않았어요", "배송 문의"),
    ("택배 운송장을 알려주세요", "배송 문의"),
    ("상품은 언제 출고되나요", "배송 문의"),
    ("상품을 환불하고 싶어요", "환불 문의"),
    ("반품 신청은 어디서 하나요", "환불 문의"),
    ("주문을 취소할 수 있나요", "환불 문의"),
    ("카드 결제가 실패했어요", "결제 문의"),
    ("입금 확인 부탁드립니다", "결제 문의"),
    ("영수증을 받고 싶어요", "결제 문의"),
    ("로그인이 되지 않아요", "계정 문의"),
    ("비밀번호를 잊어버렸어요", "계정 문의"),
    ("회원 계정을 삭제하고 싶어요", "계정 문의"),
    ("이 제품 재고가 있나요", "상품 문의"),
    ("다른 색상도 있나요", "상품 문의"),
    ("사이즈 정보를 알려주세요", "상품 문의"),
]

FAILURE_CASES = [
    "언제 받을 수 있나요",
    "돈을 다시 받고 싶어요",
    "상담원과 통화하고 싶어요",
]


def main() -> None:
    failures = []
    for text, expected in TEST_CASES:
        actual, _ = classify_intent(text)
        if actual != expected:
            failures.append((text, expected, actual))

    fallback_failures = []
    for text in FAILURE_CASES:
        actual, _ = classify_intent(text)
        if actual is not None:
            fallback_failures.append((text, actual))

    if failures or fallback_failures:
        for item in failures:
            print("분류 실패:", item)
        for item in fallback_failures:
            print("실패 사례가 예상과 다름:", item)
        raise SystemExit(1)

    print(f"정상 분류 {len(TEST_CASES)}개 확인")
    print(f"의도적으로 분류하지 못한 실패 사례 {len(FAILURE_CASES)}개 확인")


if __name__ == "__main__":
    main()
