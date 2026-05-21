# Knowledge Distillation
> Adım 31 | Tarih: 2026-05-21

## Nedir?
Büyük model (teacher) → Küçük model (student) bilgi aktarımı
Student, teacher'ın çıktılarını taklit ederek öğrenir

## Nasıl Çalışır?
1. Teacher model çıktılarını üret (soft labels/probabilities)
2. Student model, teacher'ın çıktılarına yakınsayacak şekilde eğitilir
3. Loss = α * student_loss + (1-α) * distillation_loss

## Avantajları
- Küçük model, büyük modelin performansına yakın çalışır
- Inference hızı artar
- Bellek kullanımı azalır
- Telefon için ideal

## KuroNeko İçin
- Teacher: Llama-3.2-3B veya CodeLlama-7B
- Student: KuroNeko-1B
- Distillation + QLoRA birlikte kullanılabilir
