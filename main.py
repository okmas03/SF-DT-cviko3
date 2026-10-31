from src.data import load_data, explore
from src.preprocessing import preprocess


def main():
    df = load_data()
    explore(df)
    data, Z = preprocess(df)


if __name__ == "__main__":
    main()