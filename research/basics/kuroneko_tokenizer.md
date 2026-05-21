# KuroNeko Tokenizer Kararı
> Adım 9 | Tarih: 2026-05-21

## Seçim: SentencePiece (Unigram LM)

## Gerekçe
1. Dil bağımsız — Türkçe + İngilizce + kod için ideal
2. Raw text — ön işleme gerektirmez
3. Byte fallback — bilinmeyen karakterler sorun olmaz
4. Llama uyumu — weight transfer kolay

## Vocabulary: 32,000 token
- Türkçe karakterler: ç, ğ, ı, ö, ş, ü + büyükleri
- Kod tokenları: Python, JS, Bash, JSON, YAML, Markdown
- Özel tokenlar: 16 adet

## Özel Tokenlar
| Token | Kullanım |
|-------|----------|
| <bos> | Sequence başlangıcı |
| <eos> | Sequence sonu |
| <pad> | Padding |
| <unk> | Bilinmeyen |
| <user> | Kullanıcı mesajı |
| <assistant> | Asistan yanıtı |
| <system> | System prompt |
| <code> | Kod bloğu başlangıcı |
| </code> | Kod bloğu sonu |
| <think> | Düşünce bloğu |
| </think> | Düşünce sonu |
| <tool> | Araç çağrısı |
| </tool> | Araç sonu |
| <file> | Dosya referansı |
| <search> | Arama sonucı |
| <error> | Hata mesajı |

## Eğitim Verisi
- Türkçe Wikipedia + OSCAR
- GitHub kod verisi (Python, JS, Bash)
- Özel instruction verisi
- Toplam: ~50GB ham metin

## Alternatif: Mevcut Tokenizer Kullanma
- Llama-3.2 tokenizer'ı kullanıp fine-tune
- Avantaj: Hızlı başlangıç
- Dezavantaj: Türkçe optimizasyonu zayıf
- Kararı: Önce SentencePiece, sonra karşılaştır
