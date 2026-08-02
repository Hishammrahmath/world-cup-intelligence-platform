from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.matches import router as matches_router


app = FastAPI(title="World Cup Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(matches_router)
