import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))
from retriever import PolicyRetriever


def retriever(): return PolicyRetriever(BASE_DIR / "data" / "knowledge.csv")


def test_delivery_fee_is_first():
    assert retriever().search("무료 배송 기준", 1)[0]["document_id"] == "DELIVERY-001"


def test_refund_period_is_first():
    assert retriever().search("환불 신청 기간", 1)[0]["document_id"] == "REFUND-001"


def test_empty_query_returns_empty():
    assert retriever().search("   ") == []


def test_sources_are_present():
    result = retriever().search("비밀번호", 1)[0]
    assert result["source"] and result["version"]
