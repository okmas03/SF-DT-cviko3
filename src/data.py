import pandas as pd
import matplotlib.pyplot as plt

from src.config import DATA_PATH, FIG_DIR


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def explore(df: pd.DataFrame) -> None:
    print(f"Rozmer datasetu: {df.shape[0]} používateľov, {df.shape[1]} atribútov\n")

    missing = df.isna().sum()
    print("Chýbajúce hodnoty:")
    print(missing[missing > 0], "\n")

    pd.set_option("display.width", 200)
    print("Základné štatistiky:")
    print(df.describe().T.round(2), "\n")

    # rozdelenie peňažných atribútov
    cols = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "CREDIT_LIMIT", "PAYMENTS"]
    fig, axes = plt.subplots(1, len(cols), figsize=(16, 3))
    for ax, c in zip(axes, cols):
        ax.hist(df[c].dropna(), bins=60, color="#2a78d6")
        ax.set_title(c, fontsize=9)
    fig.suptitle("Rozdelenie peňažných atribútov (pôvodné hodnoty)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "01_distribuce.png", dpi=120)
    plt.close(fig)
    print(f"Graf uložený: {FIG_DIR / '01_distribuce.png'}")