####################################################
# 10.4 Teacher Forcing: 학습 입력을 한 칸 오른쪽으로 이동
####################################################
target = ["I", "am", "a", "student", "<EOS>"]
decoder_input = ["<BOS>"] + target[:-1]
decoder_answer = target

print("=== Teacher Forcing 정렬 ===")
for step, (given, answer) in enumerate(
    zip(decoder_input, decoder_answer), 1
):
    print(f"{step}단계 입력={given:8s} 정답={answer}")

print("학습에는 정답 이전 토큰을 주지만, 추론에는 모델 출력을 다시 넣습니다.")
