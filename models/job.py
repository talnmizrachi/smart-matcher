import datetime
from dataclasses import dataclass, asdict, fields
from typing import Optional


@dataclass
class Job:
    job_id: str
    description: str
    created_time: datetime.datetime
    last_updated: datetime.datetime
    location: str
    geolocation: Optional[dict]
    summary: Optional[dict]
    title: str
    job_title_requested: str
    posting_url: str
    company_job_url: str
    company_name: str
    country: str
    salary: str
    seniority: str
    time_posted: datetime.datetime
    recommended_to: Optional[list]
    job_listing: Optional[dict]
    warm_connections: Optional[list]

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        allowed_keys = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in allowed_keys}
        return cls(**filtered_data)
