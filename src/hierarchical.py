import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics import silhouette_score

from src.config import FIG_DIR, K_RANGE


def build_linkage(Z: np.ndarray, method: str) -> np.ndarray:
    start = time.time()
    L = linkage(Z, method=method, metric="euclidean")
    print(f"Linkage '{method}' hotová za {time.time() - start:.1f} s")
    return L


def cut(L: np.ndarray, k: int) -> np.ndarray:
    """Prereže strom na k clusterov; číslovanie od 0 (fcluster čísluje od 1)."""
    return fcluster(L, k, criterion="maxclust") - 1


def evaluate_cuts(L: np.ndarray, Z: np.ndarray) -> pd.DataFrame:
    rows = []
    for k in K_RANGE:
        labels = cut(L, k)
        rows.append({
            "K": k,
            "silueta": round(silhouette_score(Z, labels), 4),
            "veľkosti": sorted(np.bincount(labels).tolist(), reverse=True),
        })
    return pd.DataFrame(rows)


def plot_dendrogram(L: np.ndarray, title: str, filename: str, p: int = 30) -> None:
    """Zobrazí len posledných p spojení – celý strom s 8 950 listami by bol nečitateľný."""
    plt.figure(figsize=(13, 4.5))
    dendrogram(L, truncate_mode="lastp", p=p, show_contracted=True,
               color_threshold=0, above_threshold_color="#2a78d6")
    plt.title(title)
    plt.xlabel("počet používateľov v uzle (v zátvorke) alebo index používateľa")
    plt.ylabel("vzdialenosť pri spojení")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=120)
    plt.close()


def plot_silhouette(res: pd.DataFrame, title: str, filename: str) -> None:
    plt.figure(figsize=(6.5, 4))
    plt.plot(res["K"], res["silueta"], marker="o", lw=2, ms=7, color="#2a78d6")
    plt.title(title)
    plt.xlabel("K")
    plt.ylabel("silhouette score")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=120)
    plt.close()