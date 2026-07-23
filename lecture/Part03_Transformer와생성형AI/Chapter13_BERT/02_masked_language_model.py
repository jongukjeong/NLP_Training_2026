####################################################
# 13.2 MLM: 가려진 토큰 후보 중 가장 높은 점수 선택
####################################################
sentence = "배송이 [MASK] 도착했어요"
logits = {"빨리": 2.1, "늦게": 0.4, "안전하게": 1.2}
prediction = max(logits, key=logits.get)

print("입력:", sentence)
print("후보 logit:", logits)
print("예측:", prediction)
print("복원:", sentence.replace("[MASK]", prediction))
