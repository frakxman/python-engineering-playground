from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.system_information_inspector.models import SystemInformation
from src.utils.system_information_inspector.report import build_report


app = FastAPI(
    title="System Information Inspector API",
    description="API for inspecting system information.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/system-information", response_model=SystemInformation)
def get_system_information():
    return build_report()
