"""
KuroNeko REST API — FastAPI tabanlı sohbet ve model bilgi servisi.

Endpoints:
    POST /chat    — Mesaj alır, cevap üretir
    GET  /health  — Servis sağlık kontrolü
    GET  /model-info — Model metadata döner

Usage:
    uvicorn kuro_api:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("kuro_api")

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="KuroNeko API",
    description="KuroNeko LLM sohbet ve model bilgi REST API",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Request / Response modelleri
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    """Sohbet istek modeli.

    Attributes:
        message: Kullanıcı mesajı (1-4096 karakter).
        temperature: Yanıt yaratıcılığı (0.0-2.0).
        max_tokens: Maksimum token sayısı (1-8192).
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=4096,
        description="Kullanıcı mesajı",
        examples=["Merhaba, nasılsın?"],
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Yanıt yaratıcılığı (0.0 = deterministik, 2.0 = yaratıcı)",
    )
    max_tokens: int = Field(
        default=512,
        ge=1,
        le=8192,
        description="Maksimum yanıt token sayısı",
    )

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        """Mesajın sadece boşluk olmadığını doğrula."""
        if not v.strip():
            raise ValueError("Mesaj sadece boşluk olamaz")
        return v.strip()


class ChatResponse(BaseModel):
    """Sohbet yanıt modeli.

    Attributes:
        reply: Model tarafından üretilen yanıt.
        request_id: Benzersiz istek takip ID'si.
        latency_ms: İşlem süresi (milisaniye).
        model: Kullanılan model adı.
    """

    reply: str = Field(..., description="Model yanıtı")
    request_id: str = Field(..., description="Benzersiz istek ID'si")
    latency_ms: float = Field(..., description="İşlem süresi (ms)")
    model: str = Field(..., description="Kullanılan model")


class HealthResponse(BaseModel):
    """Sağlık kontrol yanıt modeli."""

    status: str = Field(..., description="Servis durumu")
    uptime_seconds: float = Field(..., description="Çalışma süresi (saniye)")
    version: str = Field(..., description="API versiyonu")
    timestamp: str = Field(..., description="Sunucu zaman damgası (ISO 8601)")


class ModelInfoResponse(BaseModel):
    """Model bilgi yanıt modeli."""

    model_name: str = Field(..., description="Model adı")
    model_version: str = Field(..., description="Model versiyonu")
    parameters: str = Field(..., description="Parametre sayısı")
    context_length: int = Field(..., description="Maksimum bağlam uzunluğu")
    description: str = Field(..., description="Model açıklaması")
    capabilities: list[str] = Field(..., description="Desteklenen yetenekler")


class ErrorResponse(BaseModel):
    """Hata yanıt modeli."""

    error: str = Field(..., description="Hata türü")
    detail: str = Field(..., description="Hata detayı")
    request_id: str = Field(..., description="İstek ID'si")


# ---------------------------------------------------------------------------
# Uygulama durumu
# ---------------------------------------------------------------------------
_START_TIME: float = time.time()

# Model bilgisi — KuroNeko eğitimli model metadata
_MODEL_INFO: dict[str, Any] = {
    "model_name": "kuro-neko-7b",
    "model_version": "1.0.0",
    "parameters": "7B",
    "context_length": 8192,
    "description": "KuroNeko — Türkçe destekli, eğitimli LLM modeli",
    "capabilities": [
        "chat",
        "text-generation",
        "turkish",
        "code-assistant",
        "summarization",
    ],
}


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------
def _generate_reply(message: str, temperature: float, max_tokens: int) -> str:
    """Model yanıtı üret (placeholder).

    Gerçek implementasyonda bu fonksiyon LLM inference engine'e
    bağlanır. Şimdilik echo + metadata döner.

    Args:
        message: Kullanıcı mesajı.
        temperature: Yanıt yaratıcılığı.
        max_tokens: Maksimum token.

    Returns:
        Üretilen yanıt metni.
    """
    # TODO: Gerçek model inference entegrasyonu
    return (
        f"KuroNeko yanıtı: '{message[:80]}...' "
        f"[temp={temperature}, max_tok={max_tokens}]"
    )


def _make_request_id() -> str:
    """Benzersiz istek ID'si üret.

    Returns:
        UUIDv4 formatında string.
    """
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Exception handler
# ---------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Global HTTP exception handler.

    Args:
        request: FastAPI request nesnesi.
        exc: HTTPException instance'ı.

    Returns:
        JSON formatında hata yanıtı.
    """
    req_id = getattr(request.state, "request_id", "unknown")
    logger.warning("HTTP %d — %s [%s]", exc.status_code, exc.detail, req_id)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="http_error",
            detail=str(exc.detail),
            request_id=req_id,
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Genel exception handler — beklenmeyen hataları yakala.

    Args:
        request: FastAPI request nesnesi.
        exc: Exception instance'ı.

    Returns:
        JSON formatında genel hata yanıtı.
    """
    req_id = getattr(request.state, "request_id", "unknown")
    logger.exception("Beklenmeyen hata [%s]: %s", req_id, exc)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="internal_server_error",
            detail="Sunucu iç hatası oluştu",
            request_id=req_id,
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Middleware — request ID + timing
# ---------------------------------------------------------------------------
@app.middleware("http")
async def add_request_metadata(request: Request, call_next):
    """Her istek için request ID ve timing ekle.

    Args:
        request: FastAPI request nesnesi.
        call_next: Sonraki middleware/handler.

    Returns:
        Response with X-Request-ID header.
    """
    request_id = _make_request_id()
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.2f}"

    logger.info(
        "%s %s — %d (%.2f ms) [%s]",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
        request_id,
    )
    return response


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse, tags=["Sistem"])
async def health_check() -> HealthResponse:
    """Sağlık kontrol endpoint'i.

    Servisin çalışır durumda olup olmadığını,
    uptime'ı ve versiyon bilgisini döner.

    Returns:
        HealthResponse — status, uptime, version, timestamp.

    Raises:
        HTTPException: 503 — servis hazır değilse (henüz uygulanmadı).
    """
    uptime = time.time() - _START_TIME
    return HealthResponse(
        status="healthy",
        uptime_seconds=round(uptime, 2),
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
async def model_info() -> ModelInfoResponse:
    """Model metadata endpoint'i.

    KuroNeko modelinin teknik bilgilerini,
    yeteneklerini ve konfigürasyonunu döner.

    Returns:
        ModelInfoResponse — model adı, versiyon, parametreler, yetenekler.
    """
    return ModelInfoResponse(**_MODEL_INFO)


@app.post("/chat", response_model=ChatResponse, tags=["Sohbet"])
async def chat(request: ChatRequest) -> ChatResponse:
    """Sohbet endpoint'i.

    Kullanıcı mesajını alır, model yanıtı üretir.
    Request ID, latency ve model bilgisi ile birlikte döner.

    Args:
        request: ChatRequest — message, temperature, max_tokens.

    Returns:
        ChatResponse — reply, request_id, latency_ms, model.

    Raises:
        HTTPException: 400 — geçersiz mesaj.
        HTTPException: 500 — model yanıt üretemezse.
    """
    req_id = _make_request_id()
    start = time.perf_counter()

    logger.info(
        "Chat isteği — temp=%s, max_tok=%s [%s]",
        request.temperature,
        request.max_tokens,
        req_id,
    )

    try:
        reply = _generate_reply(
            message=request.message,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
    except Exception as exc:
        logger.exception("Model yanıt hatası [%s]", req_id)
        raise HTTPException(
            status_code=500,
            detail=f"Model yanıt üretemedi: {exc}",
        ) from exc

    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info("Chat tamamlandı — %.2f ms [%s]", latency_ms, req_id)

    return ChatResponse(
        reply=reply,
        request_id=req_id,
        latency_ms=latency_ms,
        model=_MODEL_INFO["model_name"],
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    logger.info("KuroNeko API başlatılıyor — http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
