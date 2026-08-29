from fastapi import FastAPI

from src.utils.system_information_inspector.models import SystemInformation
from src.utils.system_information_inspector.report import build_report


app = FastAPI(
    title="System Information Inspector API",
    description="API for inspecting system information.",
    version="1.0.0",
)


@app.get("/system-information", response_model=SystemInformation)
def get_system_information():
    return build_report()
