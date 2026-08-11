from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.players import router as players_router

app = FastAPI(
    title="IPL Stats API",
    description="API for aggregated IPL player statistics derived from ball-by-ball datasets.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "IPL Stats API is running"}
