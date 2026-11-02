from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "CC_GENERAL.csv"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

RANDOM_STATE = 42

FEATURES = [
    "BALANCE", "PURCHASES", "ONEOFF_PURCHASES", "INSTALLMENTS_PURCHASES", "CASH_ADVANCE",
    "PURCHASES_FREQUENCY", "CASH_ADVANCE_FREQUENCY", "CREDIT_LIMIT", "PAYMENTS", "PRC_FULL_PAYMENT",
]

# peňažné atribúty -> log transformácia
MONEY = [
    "BALANCE", "PURCHASES", "ONEOFF_PURCHASES", "INSTALLMENTS_PURCHASES", "CASH_ADVANCE",
    "CREDIT_LIMIT", "PAYMENTS",
]

K_RANGE = range(2, 11)  # rozsah pre KMeans

K_FINE = 7   # lokálne maximum siluety – jemnejšia segmentácia

# pevné poradie farieb clusterov (bezpečné aj pre farbosleposť), šum = sivá
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
NOISE_COLOR = "#9a9a96"

# názvy clusterov – určené podľa profilov (viď README)
NAMES_KM2 = {
    0: "Nakupujúci",
    1: "Používatelia hotovosti",
}
NAMES_KM7 = {
    0: "Neaktívni",
    1: "Drobní splátkoví nakupujúci",
    2: "Revolveri – nákupy aj hotovosť",
    3: "Hotovostní dlžníci",
    4: "Heavy spenders",
    5: "Príležitostní nakupujúci",
    6: "Transactors / rich savers",
}