from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

from routes.predict import router
from utils.emotion_similarity import load_model

app = FastAPI(title="AI Mood Music Recommender")

# ✅ CORS
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

# ✅ HEALTH CHECK (always available)
@app.get("/")
async def home():
    frontend_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend"
    )
    index_file = os.path.join(frontend_path, "index.html")

    # local → serve frontend
    if os.path.exists(index_file):
        return FileResponse(index_file)

    # Render → health check
    return JSONResponse({"status": "✅ Backend running on Render"})

# ✅ STATIC FILES (local only)
try:
    frontend_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend"
    )
    if os.path.exists(frontend_path):
        app.mount(
            "/static",
            StaticFiles(directory=frontend_path),
            name="static"
        )
        print("✅ Frontend mounted at /static")
    else:
        print("ℹ️ No frontend folder — running API only (Render mode)")
except Exception as e:
    print(f"⚠️ Static mount skipped: {e}")

# ✅ 404 HANDLER
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Not found"}
    )

# ✅ LOCAL RUNNER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Running on http://127.0.0.1:{port}")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )