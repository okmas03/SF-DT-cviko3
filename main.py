from src.data import load_data, explore


def main():
    df = load_data()
    explore(df)


if __name__ == "__main__":
    main()