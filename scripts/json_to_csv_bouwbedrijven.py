#!/usr/bin/env python3
import json, pandas as pd
from pathlib import Path

RAW_DIR  = Path("docs/assets/reports/bouwbedrijven-2025/_data/raw")
OUT_DIR  = Path("docs/assets/reports/bouwbedrijven-2025/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["facts"] if isinstance(data, dict) and "facts" in data else data

def to_datetime_nl(maand_str):
    mapping = {'Januari':'January','Februari':'February','Maart':'March','April':'April','Mei':'May','Juni':'June',
               'Juli':'July','Augustus':'August','September':'September','Oktober':'October','November':'November','December':'December'}
    s = maand_str
    for nl,en in mapping.items(): s = s.replace(nl, en)
    return pd.to_datetime(s, format="%B %Y")

maand = pd.DataFrame(load_json(RAW_DIR / "maandcijfers.json"))
jaar  = pd.DataFrame(load_json(RAW_DIR / "jaarcijfers.json"))

if "Sectie" in maand: maand = maand[maand["Sectie"].astype(str).str.startswith("F")]
if "Sectie" in jaar:  jaar  = jaar.dropna(subset=["Sectie"])
if "Sectie" in jaar:  jaar  = jaar[jaar["Sectie"].astype(str).str.startswith("F")]

def keep_gewest(v): return v not in ["Buitenland", "Onbekend"]

rename_m = {
    "Gewest":"Gewest","Maand":"Maand",
    "Primo-registraties":"Starters",
    "Schrappingen":"Stoppers",
    "Btw-plichtig ond. aan het einde van de maand":"Totaal_ondernemingen",
}
rename_y = {
    "Gewest":"Gewest","Jaar":"Jaar",
    "Aantal oprichtingen":"Starters",
    "Aantal schrappingen":"Stoppers",
    "Aantal btw-plichtige":"Totaal_ondernemingen",
}

maand = maand.rename(columns=rename_m)
jaar  = jaar.rename(columns=rename_y)

maand = maand[maand["Gewest"].apply(keep_gewest)].copy()
jaar  = jaar[jaar["Gewest"].apply(keep_gewest)].copy()

maand["Datum"] = maand["Maand"].apply(to_datetime_nl)
jaar["Jaar"] = pd.to_numeric(jaar["Jaar"], errors="coerce").astype("Int64")

mv = maand.groupby("Datum", as_index=False)[["Starters","Stoppers","Totaal_ondernemingen"]].sum()
yv = jaar.groupby("Jaar", as_index=False)[["Starters","Stoppers","Totaal_ondernemingen"]].sum()

mv.to_csv(OUT_DIR/"monthly_clean.csv", index=False)
yv.to_csv(OUT_DIR/"yearly_clean.csv", index=False)

mv = mv.sort_values("Datum")
mv["YoY_pct"] = mv["Totaal_ondernemingen"].pct_change(periods=12) * 100
mv[["Datum","Totaal_ondernemingen","YoY_pct"]].to_csv(OUT_DIR/"yoy_growth.csv", index=False)

print("✅ CSV's geschreven naar:", OUT_DIR)
