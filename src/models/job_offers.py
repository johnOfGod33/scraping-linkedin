from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class WorkMoel(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    FREELANCE = "Freelance"
    HYBRID = "Hybrid"


class JobOffers(BaseModel):
    title: str = Field(description="The title of the job offer")
    description: str = Field(description="the job offer description")
    company_details: dict = Field(
        description="Details about the company offering the job"
    )
    post_at: datetime = Field(description="The date the job was posted")
    applicants: int = Field(description="The number of applicants for the job")
    work_model: WorkMoel = Field(description="The work model of the job")
