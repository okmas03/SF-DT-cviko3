# Clustering používateľov kreditných kariet

Segmentácia používateľov kreditných kariet pomocou algoritmov **K-Means**, **DBSCAN** a (bonus)
**aglomeratívneho hierarchického clusteringu**. Cieľom je nájsť skupiny používateľov s podobným
správaním, charakterizovať ich a pomenovať (napr. „heavy spenders“, „rich savers“).

## Dataset

`data/cc_general.csv` obsahuje 8 950 používateľov a 18 atribútov popisujúcich používanie kreditnej
karty (zostatok, nákupy, výbery hotovosti, platby, kreditný limit, …). Popis atribútov je
v `data/dataset-vysvetlivky.xlsx`.

## Štruktúra projektu

```
├── data/              # dataset a vysvetlivky
├── figures/           # vygenerované grafy
├── src/
│   ├── config.py      # cesty a konštanty
│   └── data.py        # načítanie dát a prieskumná analýza
├── main.py            # vstupný bod
└── requirements.txt
```

## Spustenie

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Postup

### 1. Prieskum dát

- 8 950 používateľov, 18 atribútov; `CUST_ID` je iba identifikátor a pre clustering sa nepoužije.
- Chýbajúce hodnoty: `MINIMUM_PAYMENTS` (313×), `CREDIT_LIMIT` (1×).
- Peňažné atribúty sú silne pravostranne zošikmené (napr. `PURCHASES`: medián ~361, maximum ~49 000).
  Keďže oba algoritmy používajú Euklidovskú vzdialenosť, je nutná transformácia a škálovanie.
- `CASH_ADVANCE_FREQUENCY` má maximum 1,5, hoci ide o frekvenciu v rozsahu 0–1, čo je chyba v dátach.

![Rozdelenie peňažných atribútov](figures/01_distribuce.png)