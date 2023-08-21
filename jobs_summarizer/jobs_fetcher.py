from datetime import datetime
from typing import Iterator, Optional

from core.models.job import Job
from core.my_logger import get_logger
from core.utils.es_utils.elasticsearch_wrapper import ElasticsearchWrapper

logger = get_logger(__name__)

DEFAULT_LAST_X_HOURS = 24


def fetch_jobs(last_x_hours: Optional[int] = DEFAULT_LAST_X_HOURS, n_results: Optional[int] = None) -> Iterator[Job]:
    query = {
        "bool": {
            "must": [
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"title": "software engineer"}},
                            {"match_phrase": {"title": "software developer"}},
                            {"match_phrase": {"title": "backend"}},
                            {"match_phrase": {"title": "software development"}},
                            {"match_phrase": {"title": "developer"}},
                            {"match_phrase": {"title": "programmer"}}
                        ]
                    }
                },
                {"match_phrase": {"deleted": 0}},
                {"match_phrase": {"country": "Israel"}},
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"seniority": "Entry Level"}},
                            {"match_phrase": {"seniority": "Mid-Senior level"}},
                            {"match_phrase": {"seniority": "Internship"}}
                        ]
                    }
                },
                {
                    "range": {
                        "last_updated": {
                            "gte": f"now-{last_x_hours}h"
                        }
                    }
                }
            ]
        }
    }

    sort = [
        {
            "last_updated": {
                "order": "desc"
            }
        }
    ]

    elastic_searcher = ElasticsearchWrapper()
    results = elastic_searcher.search(query=query, sort=sort, n_results=n_results)

    for result in results:
        job = Job(job_id=result['unique_id'],
                  description=result.get('description', ''),
                  created_time=datetime.strptime(result.get('created', ''), "%Y-%m-%dT%H:%M:%S.%fZ"),
                  last_updated=datetime.strptime(result.get('last_updated', ''), "%Y-%m-%dT%H:%M:%S.%fZ"),
                  location=result.get('location', ''),
                  title=result.get('title', ''),
                  posting_url=result.get('url', ''),
                  company_job_url=result.get('external_url', ''),
                  company_name=result.get('company_name', ''),
                  country=result.get('country', ''),
                  salary=result.get('salary', ''),
                  seniority=result.get('seniority', ''),
                  time_posted=result.get('time_posted', ''),
                  summary=None,
                  recommended_to=[])
        yield job
