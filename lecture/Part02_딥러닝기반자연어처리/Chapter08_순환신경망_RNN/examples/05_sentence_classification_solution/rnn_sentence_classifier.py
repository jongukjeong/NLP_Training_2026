import json
from pathlib import Path
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

BASE_DIR, SEED = Path(__file__).resolve().parent, 42


def main():
    keras.utils.set_random_seed(SEED)
    df = pd.read_csv(BASE_DIR / "sentences.csv", encoding="utf-8-sig")
    train, test = train_test_split(df, test_size=0.25, stratify=df["label"], random_state=SEED)
    vectorizer = layers.TextVectorization(max_tokens=2000, output_mode="int", output_sequence_length=20)
    vectorizer.adapt(train["text"].to_numpy())
    model = keras.Sequential([keras.Input(shape=(), dtype=tf.string), vectorizer, layers.Embedding(len(vectorizer.get_vocabulary()), 32, mask_zero=True), layers.SimpleRNN(32), layers.Dense(1, activation="sigmoid")])
    model.compile(optimizer=keras.optimizers.Adam(clipnorm=1.0), loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(train["text"].to_numpy(), train["label"].to_numpy(), validation_split=0.25, epochs=25, verbose=0, callbacks=[keras.callbacks.EarlyStopping(patience=4, restore_best_weights=True)])
    metrics = model.evaluate(test["text"].to_numpy(), test["label"].to_numpy(), return_dict=True, verbose=0)
    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    model.save(out / "rnn_classifier.keras")
    (out / "metrics.json").write_text(json.dumps({k: float(v) for k, v in metrics.items()}, indent=2), encoding="utf-8")
    print(metrics)


if __name__ == "__main__": main()
