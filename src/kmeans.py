import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src.config import FIG_DIR, RANDOM_STATE, K_RANGE


def evaluate_k(Z: np.ndarray) -> pd.DataFrame:
    """Pre každé K spustí K-Means a spočíta siluetu a inerciu."""
    rows = []
    for k in K_RANGE:
        km = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE).fit(Z)
        rows.append({
            "K": k,
            "silueta": silhouette_score(Z, km.labels_, metric="euclidean"),
            "inercia": km.inertia_,
        })
        print(f"  K={k:2d}  silueta={rows[-1]['silueta']:.4f}")
    return pd.DataFrame(rows)


def plot_k_selection(res: pd.DataFrame) -> None:
    best = res.loc[res["silueta"].idxmax()]

    fig, ax = plt.subplots(1, 2, figsize=(13, 4))
    ax[0].plot(res["K"], res["silueta"], marker="o", lw=2, ms=7, color="#2a78d6")
    ax[0].scatter(best["K"], best["silueta"], s=180, facecolors="none", edgecolors="#eb6834", lw=2)
    ax[0].annotate(f"maximum: K={int(best['K'])}", (best["K"], best["silueta"]),
                   xytext=(12, -4), textcoords="offset points")
    ax[0].set_title("Silueta podľa K")
    ax[0].set_xlabel("K")
    ax[0].set_ylabel("silhouette score")
    ax[0].grid(alpha=0.3)

    ax[1].plot(res["K"], res["inercia"], marker="o", lw=2, ms=7, color="#2a78d6")
    ax[1].set_title("Inercia (SSE) podľa K – pre kontrolu")
    ax[1].set_xlabel("K")
    ax[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "04_kmeans_silueta.png", dpi=120)
    plt.close(fig)


def run_kmeans(Z: np.ndarray, k: int) -> np.ndarray:
    km = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE).fit(Z)
    print(f"K-Means K={k}: veľkosti clusterov {np.bincount(km.labels_).tolist()}")
    return km.labels_


def kmeans_analysis(Z: np.ndarray) -> np.ndarray:
    print("Voľba K podľa siluety:")
    res = evaluate_k(Z)
    plot_k_selection(res)
    best_k = int(res.loc[res["silueta"].idxmax(), "K"])
    print(f"Najlepšie K podľa siluety: {best_k}")
    return run_kmeans(Z, best_k)