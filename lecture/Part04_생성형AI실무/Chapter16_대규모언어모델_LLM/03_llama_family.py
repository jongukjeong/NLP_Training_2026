####################################################
# 16.3 Llama 계열: 공개 weight 배포 전 라이선스 점검
####################################################
model_card = {
    "name": "local-model",
    "commercial_use": True,
    "redistribution": True,
    "acceptable_use_read": False,
}
checks = {
    "상업 이용": model_card["commercial_use"],
    "재배포": model_card["redistribution"],
    "사용 정책 확인": model_card["acceptable_use_read"],
}

for label, passed in checks.items():
    print(f"{label:12s}: {'확인' if passed else '미확인'}")
print("배포 가능:", all(checks.values()))
