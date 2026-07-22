from fastapi import FastAPI

from app.api.matches import router as matches_router


app = FastAPI(title="World Cup Intelligence Platform")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(matches_router)
