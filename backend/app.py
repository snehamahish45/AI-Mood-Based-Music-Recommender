from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

from routes.predict import router
from utils.emotion_similarity import load_model

app = FastAPI(title="AI Mood Music Recommender")

# ✅ CORS — works for localhost + Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ PRE-LOAD MODEL ON STARTUP
@app.on_event("startup")
async def startup_event():
    print("🚀 Pre-loading AI model...")
    load_model()
    print("✅ Model ready!")

# ✅ ROUTES
app.include_router(router)

# ✅ SERVE FRONTEND LOCALLY (only if frontend folder exists)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")

if os.path.exists(frontend_path):
    app.mount(
        "/static",
        StaticFiles(directory=frontend_path),
        name="static"
    )

    @app.get("/")
    async def home():
        return FileResponse(
            os.path.join(frontend_path, "index.html")
        )
else:
    # ✅ RENDER — no frontend folder
    @app.get("/")
    async def health():
        return {"status": "✅ Backend running on Render"}

# ✅ 404 HANDLER
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Not found"}
    )