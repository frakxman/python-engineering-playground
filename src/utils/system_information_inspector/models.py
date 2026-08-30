from pydantic import BaseModel, Field


class SystemInformation(BaseModel):
    operating_system: str = Field(alias="Operating System")
    os_version: str = Field(alias="OS Version")
    architecture: str = Field(alias="Architecture")
    processor: str = Field(alias="Processor")
    memory: str = Field(alias="Memory")
    python: str = Field(alias="Python")
    current_time: str = Field(alias="Current Time")
