from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def softmax(x):
    shifted = x - x.max(axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=-1, keepdims=True)


def main():
    df = pd.read_csv(BASE_DIR / "tokens.csv", encoding="utf-8-sig")
    tokens = df["token"].tolist()
    vectors = df.drop(columns="token").to_numpy(dtype=float)
    weights = softmax(vectors @ vectors.T / np.sqrt(vectors.shape[1]))
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    pd.DataFrame(weights, index=tokens, columns=tokens).to_csv(out / "attention_weights.csv", encoding="utf-8-sig")
    plt.imshow(weights, cmap="Blues"); plt.xticks(range(len(tokens)), tokens); plt.yticks(range(len(tokens)), tokens); plt.colorbar(); plt.tight_layout(); plt.savefig(out / "attention_heatmap.png", dpi=160); plt.close()
    print({"tokens": len(tokens), "row_sums": weights.sum(axis=1).round(6).tolist()})


if __name__ == "__main__": main()
