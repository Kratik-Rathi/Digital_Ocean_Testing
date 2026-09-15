import logging
import time
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, Request
from app.config import LOG_LEVEL
from app.routes import health, ingest, events


# ── Logging setup ────────────────────────────────────────────
def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)

setup_logging()

# ── App setup ────────────────────────────────────────────────
app = FastAPI(title="Webhook Event Ingestion Service")

# ── Middleware ───────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    logging.getLogger(__name__).info(
        "Request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }
    )
    return response

# ── Routes ───────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(events.router)

# ── Entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    from app.config import PORT
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
