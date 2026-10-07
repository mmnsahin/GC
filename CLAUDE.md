# Görev: birleşik cevapları yaz

Bu repo, genel cerrahi sözlü çıkmış sorularından üretilen statik bir site. `index.html`, `python3 build.py` ile üretilir; elle düzenleme.

## Dosyalar
- `data/rows.json` — PDF'ten çıkarılan 383 soru. **ASLA değiştirme.** `a` alanı dosyadaki gerçek cevaptır.
- `data/clusters.json` — konu > küme > soru numaraları. Kümedeki satır sırası kaynak harflerini belirler: `rows[0]` = A, `rows[1]` = B ...
- `data/merged/<küme-id>.md` — birden fazla kez sorulmuş kümelerin birleşik cevabı. Tek kaynaklı kümeler için dosya yazma.
- Örnekler (kalite standardı): `data/merged/tiroid-02.md`, `data/merged/anorektal-01.md`. Başlamadan ikisini de oku.

## Kurallar
1. Sadece kümedeki cevaplarda yazan bilgiyi kullan. Kendi bilgini ekleme, eksik tamamlama, düzeltme yapma.
2. Cevaplardaki bilgilerin hiçbirini atlama. Aynı bilgi birden fazla cevapta varsa bir kez yaz, kaynak harflerini birleştir.
3. Her maddenin sonuna kaynak harflerini koy: `[A]`, `[A, C]`. Bu format zorunlu; build.py doğruluyor.
4. Cevaplar çelişiyorsa (sayı, sıralama, tanım) birini seçme. `> ⚠ Kaynaklar çelişiyor: ...` satırıyla iki versiyonu da yaz.
5. Soruyla ilgisiz ya da yanlış soruya verilmiş görünen cevabı silme; `> ⚠` ile not düş.
6. Boş cevaplı satırları yok say.
7. Biçim: kısa tanım paragrafı, ardından `### ` alt başlıklar, `- ` maddeler, sıra önemliyse `1. `. Kalın için `**...**`. Başka markdown kullanma (tablo, link, görsel yok).
8. Türkçe, kısa ve tıbbi terimleri koruyarak yaz. Öğrencinin konuşma dili ("sanırım", "-mış") birleşik cevapta kalmasın; ama anlamı değiştirme.

## İş akışı
- Eksik kümeleri listele: `python3 build.py --todo`
- 10'arlı gruplar halinde ilerle. Her kümede: `rows.json`'dan ilgili cevapları oku, md dosyasını yaz.
- Her grup sonunda `python3 build.py` çalıştır; hata varsa düzelt.
- Her grup sonunda commit at: `merged: <küme-id'ler>`.
- Bitince push et.

## Tek kaynaklı kümeler (data/single)
- `data/single/<küme-id>.md` — bir kez sorulmuş kümenin cevabının toparlanmış hali. Bilgi eklenmez/çıkarılmaz; sadece cümle düzeni, başlık ve tablo. Kaynak harfi yazılmaz (tek kaynak).
- Sitede bu metin gösterilir, altındaki "Soru" butonu dosyadaki değiştirilmemiş cevabı açar.
- Eksikleri listele: `python3 build.py --todo-single`
