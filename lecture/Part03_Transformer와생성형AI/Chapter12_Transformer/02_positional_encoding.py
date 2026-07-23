import math


####################################################
# 12.2 Positional Encoding: 위치마다 다른 sin/cos 값
####################################################
positions = range(4)
dimension = 4

print("=== Positional Encoding ===")
for position in positions:
    encoding = []
    for index in range(0, dimension, 2):
        angle = position / (10000 ** (index / dimension))
        encoding.extend([math.sin(angle), math.cos(angle)])
    print(position, [round(value, 4) for value in encoding])
