samples = [
    [1.0, 0.0],
    [0.8, 0.2],
    [0.1, 0.9],
]
weights = [0.7, -0.4]
bias = 0.1

print("샘플 수:", len(samples))
print("특징 수:", len(samples[0]))
print("첫 샘플:", samples[0])

predictions = []
for sample in samples:
    score = sample[0] * weights[0] + sample[1] * weights[1] + bias
    predictions.append(score)

for sample, score in zip(samples, predictions):
    print(sample, "→", round(score, 2))
