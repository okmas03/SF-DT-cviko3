import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

from src.config import FEATURES, MONEY, FIG_DIR


def select_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    # Vyberie atribúty a opraví dáta. Vracia pôvodné (netransformované) hodnoty
    # – tie neskôr sa použijú na interpretáciu clusterov.
    data = df[FEATURES].copy()
    data["CREDIT_LIMIT"] = data["CREDIT_LIMIT"].fillna(data["CREDIT_LIMIT"].median())
    data["CASH_ADVANCE_FREQUENCY"] = data["CASH_ADVANCE_FREQUENCY"].clip(upper=1)
    return data


def transform(data: pd.DataFrame) -> np.ndarray:
    # log(1 + x) na peňažné stĺpce + štandardizácia
    X = data.copy()
    X[MONEY] = np.log1p(X[MONEY])
    return StandardScaler().fit_transform(X)


def plot_correlation(data: pd.DataFrame) -> None:
    plt.figure(figsize=(9, 7))
    sns.heatmap(data.corr(), cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                annot=True, fmt=".2f", annot_kws={"size": 7}, linewidths=1, linecolor="white")
    plt.title("Korelácia vybraných atribútov")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "02_korelacia.png", dpi=120)
    plt.close()


def plot_before_after(data: pd.DataFrame, Z: np.ndarray) -> None:
    cols = ["BALANCE", "PURCHASES", "CASH_ADVANCE", "PAYMENTS"]
    fig, axes = plt.subplots(2, len(cols), figsize=(14, 5.5))
    for i, c in enumerate(cols):
        axes[0, i].hist(data[c], bins=60, color="#2a78d6")
        axes[0, i].set_title(f"{c} – pôvodné", fontsize=9)
        axes[1, i].hist(Z[:, FEATURES.index(c)], bins=60, color="#1baf7a")
        axes[1, i].set_title(f"{c} – log + z-score", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "03_transformacia.png", dpi=120)
    plt.close(fig)


def preprocess(df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    data = select_and_clean(df)
    Z = transform(data)
    plot_correlation(data)
    plot_before_after(data, Z)
    print(f"Matica pre clustering: {Z.shape[0]} riadkov × {Z.shape[1]} atribútov")
    print(f"Priemery po škálovaní ≈ 0: {np.allclose(Z.mean(axis=0), 0)}, "
          f"odchýlky ≈ 1: {np.allclose(Z.std(axis=0), 1)}")
    return data, Z