from multiprocessing import Pool
from typing import Iterator, Iterable

from jobs_summarizer import jobs_fetcher_google
from jobs_summarizer.get_v3_locations import ALL_LOCATIONS
from models.job import Job
from my_logger import get_logger
from utils.gpt_utils import gpt_utils
from utils.mongo_utils import mongo_utils

logger = get_logger(__name__)

import tiktoken


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


class JobsAnalyzer:
    def __init__(self, keywords=None):
        self.keywords = set() if keywords is None else set(keywords)

    def _summarize(self, job: Job) -> dict:
        prompt = """Output JSON Format (never output text, only JSON in this format):
    {
    "upper_salary": 100000|null,
    "lower_salary": 80000|null,
    "salary_currency": "USD"|null,
    "years_of_experience": 3|null,
    "degree_required": "true"|"false"|null,
    }
    
    If you are not sure about a field, you can leave it as null. Important: Use null and NOT None.
    
    Read the job description below and summarize the job requirements in the JSON format above:
    ####
    %s 
    %s
    ####""" % (job.title + " " + job.location, job.description[:20000])

        # Count the number of tokens in the prompt
        # num_tokens = num_tokens_from_messages([{"content": prompt}])

        # # if the number of tokens is too large, we need to trim the prompt
        # if num_tokens > 8000:
        #     logger.warning(f"Prompt is too long ({num_tokens} tokens). Trimming prompt.")
        #     prompt = prompt[:25000]
        #     num_tokens = num_tokens_from_messages([{"content": prompt}])
        #     logger.warning(f"New prompt is {num_tokens} tokens.")

        logger.info(f"Summarizing job {job.title}")
        summary = gpt_utils.get_response_from_gpt(
            system="You are an assistant that extracts data as JSON from job descriptions.",
            prompt=prompt,
            is_json=True)

        if not summary:
            logger.error(f'Problem with ChatGPT: {summary}')
            return {}

        # new_keywords = []
        # for field in ['nice_to_have_requirements', 'must_have_requirements']:
        #     if field not in summary:
        #         logger.error(f'Problem with ChatGPT: {summary}')
        #         return {}
        #     summary[field] = [keyword.lower().replace(' ', '_').replace('-', '_') for keyword in summary[field]]
        #     summary[field] = [keyword for keyword in summary[field] if len(keyword) < 30]
        #     new_keywords += summary[field]

        # logger.debug(f"New keywords: {set(new_keywords) - self.keywords}")

        # self.keywords = self.keywords.union(new_keywords)
        # mongo_utils.store_config('keywords', list(self.keywords))  # save the new keywords to the DB

        return summary

    def _summarize_jobs(self, jobs: Iterable[Job]) -> Iterator[Job]:
        for job in jobs:
            job.summary = self._summarize(job)
            yield job

    # def _filter_jobs(self, jobs: Iterable[Job]) -> List[Job]:
    #     # Filter jobs that already exist in the DB
    #     jobs_company_urls = [job.company_job_url for job in jobs]
    #     jobs_in_db_company_urls = [job.company_job_url for job in
    #                                mongo_utils.get_jobs_by_company_urls(jobs_company_urls)]  # get existing jobs in DB
    #     return [job for job in jobs if
    #             job.company_job_url not in jobs_in_db_company_urls]  # filter only jobs that are not in DB

    def process_job(self, data):
        job_title, location = data
        jobs = list(jobs_fetcher_google.fetch_jobs(job_title, location))
        logger.info(f"Inserting {len(jobs)} jobs to DB...")
        for job in jobs:
            logger.debug("Inserting job to db...")
            mongo_utils.store_job(job)


def main():
    # extractor = JobsAnalyzer(keywords=mongo_utils.load_config('keywords'))
    extractor = JobsAnalyzer(keywords=[])
    job_titles = ["Marketing Analyst"]
    locations = ["Tel Aviv"]

    logger.info(f"List of locations: {locations}")

    data = [(job_title, location) for job_title in job_titles for location in locations]

    with Pool() as p:
        p.map(extractor.process_job, data)


if __name__ == "__main__":
    main()
