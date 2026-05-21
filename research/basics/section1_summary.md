# Bölüm 1 Özeti — LLM Temelleri
> Adım 10 | Tarih: 2026-05-21

## Tamamlanan Adımlar
1. ✅ Transformer mimarisini araştır → transformer_basics.md
2. ✅ Tokenizer türlerini araştır → tokenizer_guide.md
3. ✅ LLMs-from-scratch reposunu incele → llm_from_scratch_notes.md
4. ✅ nanoGPT reposunu incele → nanogpt_notes.md
5. ✅ Embedding ve positional encoding → embeddings.md
6. ✅ Attention mekanizması derinlemesine → attention.md
7. ✅ FFN, layer norm, residual → ffn_norm_residual.md
8. ✅ KuroNeko mimarisi tasarla → kuroneko_arch.md
9. ✅ KuroNeko tokenizer seç → kuroneko_tokenizer.md

## Önemli Kararlar
- **Mimari:** Decoder-only transformer
- **Parametre:** 1.1B (telefonda çalışır, Kaggle'da eğitilir)
- **Positional Encoding:** RoPE (Llama uyumlu)
- **Attention:** GQA (Grouped Query Attention) + Flash Attention
- **Aktivasyon:** SwiGLu
- **Normalizasyon:** RMSNorm (pre-norm)
- **Tokenizer:** SentencePiece (Unigram LM), 32K vocab
- **Context:** 4096 token

## Oluşturulan Dosyalar
- transformer_basics.md
- tokenizer_guide.md
- llm_from_scratch_notes.md
- nanogpt_notes.md
- embeddings.md
- attention.md
- ffn_norm_residual.md
- kuroneko_arch.md
- kuroneko_tokenizer.md
