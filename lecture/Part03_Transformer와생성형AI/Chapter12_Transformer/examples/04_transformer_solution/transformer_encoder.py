import json
from pathlib import Path
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

BASE_DIR = Path(__file__).resolve().parent


class TransformerBlock(layers.Layer):
    def __init__(self, dim=32, heads=4, ff_dim=64):
        super().__init__(); self.att = layers.MultiHeadAttention(num_heads=heads, key_dim=dim // heads); self.ffn = keras.Sequential([layers.Dense(ff_dim, activation="relu"), layers.Dense(dim)]); self.norm1 = layers.LayerNormalization(); self.norm2 = layers.LayerNormalization(); self.drop1 = layers.Dropout(0.1); self.drop2 = layers.Dropout(0.1)
    def call(self, x, training=False):
        a = self.att(x, x); x = self.norm1(x + self.drop1(a, training=training)); f = self.ffn(x); return self.norm2(x + self.drop2(f, training=training))


def main():
    keras.utils.set_random_seed(42)
    df = pd.read_csv(BASE_DIR / "sequences.csv")
    x = tf.constant([[int(v) for v in row.split()] for row in df["sequence"]], dtype=tf.int32); y = df["label"].to_numpy()
    inputs = keras.Input(shape=(6,), dtype="int32"); token = layers.Embedding(20, 32)(inputs); positions = layers.Embedding(6, 32)(tf.range(6)); z = TransformerBlock()(token + positions); z = layers.GlobalAveragePooling1D()(z); outputs = layers.Dense(1, activation="sigmoid")(z)
    model = keras.Model(inputs, outputs); model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]); model.fit(x, y, epochs=30, verbose=0)
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True); model.save(out / "transformer_encoder.keras"); metrics = model.evaluate(x, y, return_dict=True, verbose=0); (out / "metrics.json").write_text(json.dumps({k: float(v) for k, v in metrics.items()}, indent=2), encoding="utf-8"); print(metrics)


if __name__ == "__main__": main()
