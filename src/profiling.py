import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

from src.config import FEATURES, FIG_DIR, PALETTE, NOISE_COLOR, RANDOM_STATE


def _label(c, names):
    if c == -1:
        return "šum"
    return f"{c}: {names[c]}" if names else str(c)


def profile(data: pd.DataFrame, labels: np.ndarray, names: dict | None = None) -> pd.DataFrame:
    """Mediány pôvodných hodnôt + veľkosť a podiel clustera."""
    g = data.assign(cluster=labels).groupby("cluster")
    prof = g.median().round(2)
    prof.insert(0, "počet", g.size())
    prof.insert(1, "podiel %", (g.size() / len(labels) * 100).round(1))
    prof.index = [_label(c, names) for c in prof.index]
    return prof


def plot_profile_heatmap(Z, labels, names, title, filename):
    """Priemerný z-score atribútov v clustri: > 0 nadpriemer, < 0 podpriemer."""
    zm = pd.DataFrame(Z, columns=FEATURES).assign(cluster=labels).groupby("cluster").mean()
    zm.index = [_label(c, names) for c in zm.index]

    plt.figure(figsize=(12, 0.55 * len(zm) + 2))
    sns.heatmap(zm, cmap="RdBu_r", center=0, vmin=-2, vmax=2, annot=True, fmt=".1f",
                linewidths=1.5, linecolor="white", cbar_kws={"label": "z-score"})
    plt.title(title)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=120)
    plt.close()


def plot_pca(Z, labels, names, title, filename):
    """2D projekcia (PCA) – iba na vizualizáciu, clustering beží na všetkých dimenziách."""
    P = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(Z)

    fig, ax = plt.subplots(figsize=(8, 6))
    for c in sorted(set(labels)):
        m = labels == c
        if c == -1:
            ax.scatter(P[m, 0], P[m, 1], s=10, c=NOISE_COLOR, marker="x", alpha=0.6,
                       label=f"šum ({m.sum()})")
        else:
            ax.scatter(P[m, 0], P[m, 1], s=6, color=PALETTE[c % len(PALETTE)], alpha=0.5,
                       label=f"{_label(c, names)} ({m.sum()})")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title(title)
    ax.legend(markerscale=2.5, fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=120)
    plt.close(fig)


def describe_clusters(data, Z, labels, names, title, prefix):
    """Vypíše profil a uloží heatmapu + PCA graf."""
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 20)
    print(f"\n=== {title} – mediány pôvodných hodnôt ===")
    print(profile(data, labels, names).to_string())
    plot_profile_heatmap(Z, labels, names, f"{title} – profil clusterov (priemerný z-score)",
                         f"{prefix}_profil.png")
    plot_pca(Z, labels, names, f"{title} (PCA projekcia)", f"{prefix}_pca.png")