# Pruning Teknikleri
> Adım 32 | Tarih: 2026-05-21

## Nedir?
Model ağırlıklarının gereksiz kısımlarının çıkarılması

## Türleri

### Unstructured Pruning
- Bireysel ağırlıklar sıfırlanır
- %50-90 parametre azaltma
- Özel hardware gerektirir (sparse computation)

### Structured Pruning
- Tam katman, head veya nöron çıkarılır
- Donanımdan bağımsız hızlanma
- Daha az agresif (%20-50 azaltma)

### Attention Head Pruning
- Önemli olmayan attention head'leri çıkar
- Bazı head'ler gereksiz olabilir (Flan-T5'te %40 head prune edilebilir)

## Iterative Pruning
1. Modeli eğit
2. Önemli ağırlıkları belirle
3. Düşük önemlileri çıkar
4. Fine-tune et
5. Tekrarla

## KuroNeko İçin
- QLoRA sonrası structured pruning düşünülebilir
- İlk aşamada pruning yok (QLoRA yeterli)
- v2'de değerlendirilebilir
