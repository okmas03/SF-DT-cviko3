from src.data import load_data, explore
from src.preprocessing import preprocess
from src.kmeans import kmeans_analysis


def main():
    df = load_data()
    explore(df)
    data, Z = preprocess(df)
    labels_km = kmeans_analysis(Z)


if __name__ == "__main__":
    main()