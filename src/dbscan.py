import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator

from src.config import FIG_DIR, MIN_PTS_FACTOR


def k_distance(Z: np.ndarray, min_pts: int) -> np.ndarray:
    """Zoradené vzdialenosti každého bodu k jeho MinPts-tému susedovi (vrátane seba)."""
    nn = NearestNeighbors(n_neighbors=min_pts, metric="euclidean").fit(Z)
    distances, _ = nn.kneighbors(Z)
    return np.sort(distances[:, -1])


def find_eps(kdist: np.ndarray) -> tuple[float, int]:
    """Lakeť k-distance krivky (metóda Kneedle)."""
    knee = KneeLocator(np.arange(len(kdist)), kdist, curve="convex", direction="increasing")
    return float(kdist[knee.knee]), int(knee.knee)


def plot_k_distance(kdist, eps, knee_idx, min_pts):
    fig, ax = plt.subplots(1, 2, figsize=(13, 4))
    for a, start in zip(ax, [0, 7500]):
        x = np.arange(start, len(kdist))
        a.plot(x, kdist[start:], lw=2, color="#2a78d6")
        a.axhline(eps, color="#eb6834", ls="--", lw=1.5)
        a.scatter([knee_idx], [eps], s=90, color="#eb6834", zorder=3)
        a.annotate(f"lakeť: Eps ≈ {eps:.2f}", (knee_idx, eps),
                   xytext=(-150, 25), textcoords="offset points")
        a.set_xlabel("body zoradené podľa k-distance")
        a.set_ylabel(f"vzdialenosť k {min_pts}. susedovi")
        a.grid(alpha=0.3)
    ax[0].set_title("k-distance graf")
    ax[1].set_title("detail konca krivky")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "07_dbscan_k_distance.png", dpi=120)
    plt.close(fig)


def run_dbscan(Z: np.ndarray, eps: float, min_pts: int) -> np.ndarray:
    labels = DBSCAN(eps=eps, min_samples=min_pts, metric="euclidean").fit_predict(Z)
    n_clusters = len(set(labels) - {-1})
    n_noise = int((labels == -1).sum())
    print(f"DBSCAN Eps={eps:.2f}, MinPts={min_pts}: clusterov={n_clusters}, "
          f"šum={n_noise} ({n_noise / len(labels):.1%})")
    return labels


def dbscan_analysis(Z: np.ndarray) -> tuple[np.ndarray, float, int]:
    min_pts = MIN_PTS_FACTOR * Z.shape[1]
    kdist = k_distance(Z, min_pts)
    eps, knee_idx = find_eps(kdist)
    print(f"\nDBSCAN – MinPts = {min_pts}, Eps (lakeť) = {eps:.3f}")
    plot_k_distance(kdist, eps, knee_idx, min_pts)
    return run_dbscan(Z, eps, min_pts), eps, min_pts