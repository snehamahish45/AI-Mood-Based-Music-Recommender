from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.routes.predict import router

app = FastAPI()

# ✅ CORS (for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ BASE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 👉 frontend folder inside backend
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ✅ DEBUG (optional but useful)
print("Frontend path:", FRONTEND_DIR)

# ✅ STATIC FILES (JS, CSS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ✅ SERVE MAIN PAGE
@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# ✅ INCLUDE API ROUTES
app.include_router(router)