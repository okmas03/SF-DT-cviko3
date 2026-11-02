import pandas as pd

from src.config import K_FINE, NAMES_KM2, NAMES_KM7
from src.data import load_data, explore
from src.preprocessing import preprocess
from src.kmeans import kmeans_analysis, run_kmeans
from src.profiling import describe_clusters


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


if __name__ == "__main__":
    main() 