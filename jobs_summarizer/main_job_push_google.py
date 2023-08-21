from core.config import get_setting
from core.jobs_summarizer.most_common_locations import uk_locations, us_locations, canada_locations, \
    australia_locations, germany_locations, israel_locations
from core.my_logger import get_logger
from core.utils.google_utils import maps
from core.utils.mongo_utils.mongo_utils import get_jobs_with_filters
from core.utils.slack_utils import slack_api

logger = get_logger(__name__)


def get_and_send_jobs(job_title, location, channel, hours_ago=12, distance=400):
    google_api_client = maps.create_googlemaps_client(get_setting('GOOGLE_API'))
    geolocation = maps.geocode_address(google_api_client, location)

    filters = {
        "hours": hours_ago,
        "job_title_requested": job_title,
    }

    results = get_jobs_with_filters(filters)

    for job in results:
        if job.geolocation and maps.are_geo_locations_proximate(job.geolocation, geolocation, distance):
            # TODO: check how to do that for remote jobs
            slack_api.send_job_to_slack(job, slack_id=channel)
        else:
            logger.info(f"Job {job.title} at {job.location.strip()} is not within {distance} km of {location}")


if __name__ == '__main__':
    channels = {
        '#cyber-job-search-israel': israel_locations,
        '#cyber-job-search-uk': uk_locations,
        '#cyber-job-search-us': us_locations,
        '#cyber-job-search-canada': canada_locations,
        '#cyber-job-search-australia': australia_locations,
        '#cyber-job-search-germany': germany_locations,

        '#se-jobs-uk': uk_locations,
        '#se-jobs-us': us_locations,
        '#se-jobs-canada': canada_locations,
        '#se-jobs-australia': canada_locations,
        '#se-jobs-germany': canada_locations,
        '#se-jobs-israel': israel_locations,
        #
        # '#data-analyst-jobs-uk': uk_locations,
        # '#data-analyst-jobs-us': us_locations,
        # '#data-analyst-jobs-canada': canada_locations,
        # '#data-analyst-jobs-australia': australia_locations,
        # '#data-analyst-jobs-germany': germany_locations,
        # '#data-analyst-jobs-israel': israel_locations,

        'web-job-search-uk': uk_locations,
        'web-job-search-us-east': us_locations,
        'web-job-search-eu': uk_locations,
        'web-job-search-israel': israel_locations

    }

    for channel, locations in channels.items():
        for location in locations:
            if 'cyber' in channel:
                get_and_send_jobs("Cyber Security Analyst", location, channel)

            elif 'se-' in channel:
                get_and_send_jobs("Software Engineer", location, channel)
            elif 'web-' in channel:
                get_and_send_jobs("Software Engineer", location, channel)
            elif 'data' in channel:
                get_and_send_jobs("Data Analyst", location, channel)
            else:
                print("Channel not found {}".format(channel))
                continue
