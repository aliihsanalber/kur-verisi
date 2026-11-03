# kur-verisi

TCMB'nin her iş günü yayımladığı **döviz alış ve satış kurlarını** (EUR, USD) `kur.json` dosyasında tutar.
Bir GitHub Actions görevi bu dosyayı iş günleri otomatik olarak günceller. Dosya, tarayıcıda çalışan uygulamaların
doğrudan okuyabilmesi için herkese açık bir adreste durur (TCMB sitesi tarayıcıdan doğrudan okunamaz).

- Kaynak: https://www.tcmb.gov.tr/kurlar/today.xml (TCMB'nin herkese açık verisi)
- Adres: `https://raw.githubusercontent.com/aliihsanalber/kur-verisi/main/kur.json`
- İçinde yalnızca kur bilgisi vardır. Başka bir veri, kullanıcı bilgisi ya da gizli anahtar yoktur.

Bu veri bilgi amaçlıdır, resmî belge yerine geçmez.
