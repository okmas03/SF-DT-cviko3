from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "CC_GENERAL.csv"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

RANDOM_STATE = 42
MIN_PTS_FACTOR = 2 
K_RANGE = range(2, 11)  # rozsah pre KMeans
K_FINE = 7   # lokálne maximum siluety – jemnejšia segmentácia
EPS_GRID = [0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0]
EPS_ALT = 1.0

FEATURES = [
    "BALANCE", "PURCHASES", "ONEOFF_PURCHASES", "INSTALLMENTS_PURCHASES", "CASH_ADVANCE",
    "PURCHASES_FREQUENCY", "CASH_ADVANCE_FREQUENCY", "CREDIT_LIMIT", "PAYMENTS", "PRC_FULL_PAYMENT",
]

# peňažné atribúty -> log transformácia
MONEY = [
    "BALANCE", "PURCHASES", "ONEOFF_PURCHASES", "INSTALLMENTS_PURCHASES", "CASH_ADVANCE",
    "CREDIT_LIMIT", "PAYMENTS",
]

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

NAMES_DB = {0: "Hlavný zhluk"}

NAMES_DB_ALT = {
    0: "Bežní nakupujúci",
    1: "Hotovostní dlžníci",
    2: "Revolveri – nákupy aj hotovosť",
    3: "Hotovosť bez splácania",
    4: "VIP – veľké nákupy, plne splácajú",
    5: "Menšie nákupy, plne splácajú",
}