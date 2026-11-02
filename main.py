import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

from src.config import (K_FINE, NAMES_KM2, NAMES_KM7, NAMES_DB, NAMES_DB_ALT, FEATURES,
                        EPS_GRID, EPS_ALT, K_WARD, NAMES_WARD)
from src.data import load_data, explore
from src.preprocessing import preprocess
from src.kmeans import kmeans_analysis, run_kmeans
from src.profiling import describe_clusters
from src.dbscan import dbscan_analysis, eps_sensitivity, plot_eps_sensitivity, run_dbscan
from src.hierarchical import build_linkage, cut, evaluate_cuts, plot_dendrogram, plot_silhouette

def main():
    df = load_data()
    explore(df)
    data, Z = preprocess(df)

    # K-Means
    labels_km2 = kmeans_analysis(Z)              # K podľa maxima siluety (= 2)
    labels_km7 = run_kmeans(Z, K_FINE)           # lokálne maximum siluety
    describe_clusters(data, Z, labels_km2, NAMES_KM2, "K-Means K=2", "05_kmeans_k2")
    describe_clusters(data, Z, labels_km7, NAMES_KM7, "K-Means K=7", "06_kmeans_k7")

    print("\nAko sa K=2 rozpadne na K=7:")
    print(pd.crosstab(pd.Series(labels_km2, name="K=2").map(NAMES_KM2),
                      pd.Series(labels_km7, name="K=7").map(NAMES_KM7)))

    # DBSCAN
    labels_db, eps, min_pts = dbscan_analysis(Z)
    describe_clusters(data, Z, labels_db, NAMES_DB,
                      f"DBSCAN Eps={eps:.2f}, MinPts={min_pts}", "08_dbscan")

    print("\nOutliery (šum) podľa DBSCAN:")
    print(df.loc[labels_db == -1, ["CUST_ID"] + FEATURES].round(2).to_string())

    # DBSCAN – citlivosť na Eps
    print("\nCitlivosť DBSCAN na Eps (MinPts = 20):")
    sens = eps_sensitivity(Z, min_pts, EPS_GRID)
    print(sens.to_string(index=False))
    plot_eps_sensitivity(sens)

    labels_db_alt = run_dbscan(Z, EPS_ALT, min_pts)
    describe_clusters(data, Z, labels_db_alt, NAMES_DB_ALT,
                      f"DBSCAN Eps={EPS_ALT}, MinPts={min_pts}", "10_dbscan_eps1")

    # Hierarchický clustering – centroid linkage (podľa zadania)
    print("\n=== Hierarchický clustering – centroid linkage ===")
    L_centroid = build_linkage(Z, "centroid")
    plot_dendrogram(L_centroid, "Dendrogram – centroid linkage (posledných 30 spojení)",
                    "11_hier_centroid_dendrogram.png")
    print(evaluate_cuts(L_centroid, Z).to_string(index=False))

    labels_c6 = cut(L_centroid, 6)
    sizes = np.bincount(labels_c6)
    small = [c for c in range(len(sizes)) if sizes[c] < 300]
    print("\nMalé clustery pri K=6 (centroid):")
    print(df.loc[np.isin(labels_c6, small), ["CUST_ID"] + FEATURES]
            .assign(cluster=labels_c6[np.isin(labels_c6, small)])
            .sort_values("cluster").head(15).round(2).to_string())

    # Hierarchický clustering – Ward
    print("\n=== Hierarchický clustering – Ward ===")
    L_ward = build_linkage(Z, "ward")
    plot_dendrogram(L_ward, "Dendrogram – Ward (posledných 30 spojení)",
                    "12_hier_ward_dendrogram.png")
    res_ward = evaluate_cuts(L_ward, Z)
    print(res_ward.to_string(index=False))
    plot_silhouette(res_ward, "Ward – silueta podľa K", "12_hier_ward_silueta.png")

    labels_ward = cut(L_ward, K_WARD)
    describe_clusters(data, Z, labels_ward, NAMES_WARD, f"Ward K={K_WARD}", "13_ward_k6")

    print(f"\nZhoda Ward K={K_WARD} a K-Means K=7 (ARI): "
          f"{adjusted_rand_score(labels_km7, labels_ward):.3f}")
    print(pd.crosstab(pd.Series(labels_ward, name="Ward").map(NAMES_WARD),
                      pd.Series(labels_km7, name="K-Means K=7").map(NAMES_KM7)))


if __name__ == "__main__":
    main()