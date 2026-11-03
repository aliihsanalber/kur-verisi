#!/usr/bin/env python3
"""TCMB'nin yayımladığı günlük döviz kurlarından kur.json üretir.

Yalnızca Python standart kütüphanesini kullanır. Kaynak: https://www.tcmb.gov.tr/kurlar/today.xml
kur.json biçimi:
{
  "kaynak": "TCMB", "kurTuru": "Döviz Alış / Döviz Satış",
  "tarih": "2026-10-20",            # TCMB'nin kuru yayımladığı iş günü
  "guncellendi": "2026-10-20T12:47:10Z",
  "eur": {"alis": 55.5191, "satis": 55.6191},
  "usd": {"alis": 47.xx, "satis": 47.xx}
}
"""
import json, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

URL = "https://www.tcmb.gov.tr/kurlar/today.xml"


def indir():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (kur-verisi)"})
    return urllib.request.urlopen(req, timeout=60).read()


def oku(xml_bytes):
    kok = ET.fromstring(xml_bytes)
    tarih = datetime.strptime(kok.get("Date"), "%m/%d/%Y").date().isoformat()
    sonuc = {}
    for c in kok.findall("Currency"):
        kod = c.get("CurrencyCode")
        if kod in ("EUR", "USD"):
            alis, satis = float(c.find("ForexBuying").text), float(c.find("ForexSelling").text)
            sonuc[kod.lower()] = {"alis": alis, "satis": satis}
    if set(sonuc) != {"eur", "usd"}:
        raise ValueError("EUR veya USD bulunamadı")
    return tarih, sonuc


def makul(sonuc):
    """Bariz hatalı veriyi (sıfır, eksi, alış > satış, aşırı fark) yayımlamaz."""
    for k, v in sonuc.items():
        if not (0.5 < v["alis"] < 1000 and v["alis"] <= v["satis"] <= v["alis"] * 1.05):
            raise ValueError("Makul olmayan kur: %s %s" % (k, v))


def main():
    tarih, sonuc = oku(indir())
    makul(sonuc)
    cikti = {
        "kaynak": "TCMB",
        "kurTuru": "Döviz Alış / Döviz Satış",
        "tarih": tarih,
        "guncellendi": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "eur": sonuc["eur"],
        "usd": sonuc["usd"],
    }
    # Değişen bir şey yoksa dosyayı yeniden yazma (gereksiz commit olmasın)
    try:
        eski = json.load(open("kur.json", encoding="utf-8"))
        if eski.get("tarih") == tarih and eski.get("eur") == cikti["eur"] and eski.get("usd") == cikti["usd"]:
            print("Değişiklik yok:", tarih)
            return
    except (OSError, ValueError):
        pass
    with open("kur.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(cikti, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("Güncellendi:", tarih, cikti["eur"], cikti["usd"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:      # noqa: BLE001
        print("HATA:", e, file=sys.stderr)
        sys.exit(1)
