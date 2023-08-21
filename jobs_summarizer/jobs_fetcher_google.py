from datetime import datetime
from typing import Iterator

from config import get_setting
from models.job import Job
from my_logger import get_logger
from utils.google_utils import maps
from utils.serp_utils.serp_search import get_new_jobs, convert_relative_date_to_utc

logger = get_logger(__name__)


def fetch_jobs(job_title, location) -> Iterator[Job]:
    logger.info(f"Fetching jobs for {job_title} in {location}")
    results = get_new_jobs(job_title, location)

    googlemaps_client = maps.create_googlemaps_client(get_setting('GOOGLE_API'))

    for result in results:
        if not result.get('location'):
            continue

        geolocation = maps.geocode_address(googlemaps_client, result.get('location'))

        try:
            job = Job(job_id=result.get('job_id'),
                      description=result.get('description'),
                      created_time=datetime.utcnow(),
                      last_updated=datetime.utcnow(),
                      location=result.get('location'),
                      geolocation=geolocation,
                      summary=result,
                      title=result.get('title'),
                      job_title_requested=job_title,
                      posting_url="",
                      company_job_url=result.get('job_listing').get('apply_options')[0]['link'],
                      company_name=result.get('company_name'),
                      country="",
                      salary="",
                      seniority="",
                      time_posted=convert_relative_date_to_utc(result.get('detected_extensions').get('posted_at')),
                      recommended_to=[],
                      job_listing=result.get('job_listing'),
                      warm_connections=result.get('warm_connections'))

            yield job
        except Exception as e:
            logger.error(f"Failed to create job from result: {result}")
            logger.exception(e)
            continue
