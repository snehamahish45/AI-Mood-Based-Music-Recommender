from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routes.predict import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# frontend folder
app.mount("/static", StaticFiles(directory="backend/frontend"), name="static")


@app.get("/")
async def home():
    return FileResponse("backend/frontend/index.html")
