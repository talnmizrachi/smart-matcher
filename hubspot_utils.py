import os
from collections import Counter

import numpy
import numpy as np
import requests
from hubspot.crm.contacts import BatchInputSimplePublicObjectBatchInput
from hubspot.crm.objects.notes import BatchInputSimplePublicObjectInputForCreate
from hubspot import HubSpot
from hubspot.crm.contacts import PublicObjectSearchRequest, SimplePublicObjectInputForCreate, ApiException

from core.config import get_setting
from core.my_logger import get_logger

logger = get_logger(__name__)

TOKENS_FILE = os.path.join(os.path.dirname(__file__), 'tokens.json')
HUBSPOT_BATCH_SIZE = 100


def init_api_client():
    return HubSpot(access_token=get_setting("HUBSPOT_TOKEN"))


# Initialize the HubSpot API client
def find_contact_by_email(api_client, email):
    """Search for a contact by email."""
    search_request = PublicObjectSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "value": email,
                        "propertyName": "email",
                        "operator": "EQ"
                    }
                ]
            }
        ],
        limit=1
    )

    try:
        response = api_client.crm.contacts.search_api.do_search(public_object_search_request=search_request)
        if response.results:
            return response.results[0]
        return None
    except ApiException as e:
        logger.error(f"Exception when searching for contact by email: {e}")
        return None


def update_contact(api_client, contact_id, properties):
    """Update a contact's information."""

    contact_input = SimplePublicObjectInputForCreate(properties=properties)

    try:
        api_client.crm.contacts.basic_api.update(contact_id, simple_public_object_input=contact_input)
    except ApiException as e:
        logger.error(f"Exception when updating contact: {e}")


def create_contact(api_client, properties):
    """Create a new contact."""
    contact_input = SimplePublicObjectInputForCreate(properties=properties)
    try:
        api_client.crm.contacts.basic_api.create(simple_public_object_input_for_create=contact_input)
    except ApiException as e:
        logger.error(f"Exception when creating contact: {e}")


def handle_new_contact(api_client, properties):
    contact = find_contact_by_email(api_client, properties['email'])

    if contact:
        logger.info(f"Contact with email {properties['email']} found. Updating information...")
        update_contact(api_client, contact.id, properties)
    else:
        logger.info(f"Contact with email {properties['email']} not found. Creating a new contact...")
        create_contact(api_client, properties)


def get_swe_contacts(api_client,
                     properties=None,
                     additional_filters=None,
                     properties_with_history=None):
    if properties is None:
        properties = ["email"]

    must_properties = ['email', 'firstname', 'lastname']
    for prop_name in must_properties:
        if prop_name not in properties:
            properties.append(prop_name)

    # set filters
    filters = [
        {
            "value": "Software Engineering",
            "propertyName": "current_enrollment_program",
            "operator": "EQ"
        },
        {
            "value": "January 2023",
            "propertyName": "current_cohort",
            "operator": "EQ"
        }
    ]

    if additional_filters is not None:
        filters = filters + additional_filters

    total = numpy.Inf
    retrieved_contacts = []
    while len(retrieved_contacts) < total:
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[
                {
                    "filters": filters
                }
            ],
            properties=properties,
            limit=100,
            after=len(retrieved_contacts)
        )

        api_response = api_client.crm.contacts.search_api.do_search(
            public_object_search_request=public_object_search_request,
        )
        total = api_response.total
        retrieved_contacts += api_response.results

    contacts_dict = {
        contact.properties['email']: contact
        for contact in retrieved_contacts
    }

    # Update properties with history
    if properties_with_history:
        n_chunks = len(contacts_dict.keys()) // 50 + 1
        for i, batch in enumerate(np.array_split(list(contacts_dict.keys()), n_chunks)):
            params = {
                "inputs": [{"id": contacts_dict[email].id} for email in batch],
                "propertiesWithHistory": properties_with_history
            }

            data = requests.post('https://api.hubapi.com/crm/v3/objects/contacts/batch/read',
                                 json=params,
                                 headers={"Authorization": f"Bearer {api_client.access_token}"}).json()
            for contact in data['results']:
                contacts_dict[contact['properties']['email']].properties_with_history = contact['propertiesWithHistory']

    return contacts_dict


def get_contacts(api_client,
                 domain,
                 cohort,
                 properties=None,
                 additional_filters=None,
                 properties_with_history=None):
    if properties is None:
        properties = ["email"]

    must_properties = ['email', 'firstname', 'lastname']
    for prop_name in must_properties:
        if prop_name not in properties:
            properties.append(prop_name)

    # set filters
    filters = [
        {
            "value": domain,
            "propertyName": "current_enrollment_program",
            "operator": "EQ"
        },
        {
            "value": cohort,
            "propertyName": "current_cohort",
            "operator": "EQ"
        }
    ]

    if additional_filters is not None:
        filters = filters + additional_filters

    total = numpy.Inf
    retrieved_contacts = []
    while len(retrieved_contacts) < total:
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[
                {
                    "filters": filters
                }
            ],
            properties=properties,
            limit=100,
            after=len(retrieved_contacts)
        )

        api_response = api_client.crm.contacts.search_api.do_search(
            public_object_search_request=public_object_search_request,
        )
        total = api_response.total
        retrieved_contacts += api_response.results

    contacts_dict = {
        contact.properties['email']: contact
        for contact in retrieved_contacts
    }

    # Update properties with history
    if properties_with_history:
        n_chunks = len(contacts_dict.keys()) // 50 + 1
        for i, batch in enumerate(np.array_split(list(contacts_dict.keys()), n_chunks)):
            params = {
                "inputs": [{"id": contacts_dict[email].id} for email in batch],
                "propertiesWithHistory": properties_with_history
            }

            data = requests.post('https://api.hubapi.com/crm/v3/objects/contacts/batch/read',
                                 json=params,
                                 headers={"Authorization": f"Bearer {api_client.access_token}"}).json()
            for contact in data['results']:
                contacts_dict[contact['properties']['email']].properties_with_history = contact['propertiesWithHistory']

    return contacts_dict


def batch_update(api_client, inputs):
    n_chunks = len(inputs) // HUBSPOT_BATCH_SIZE + 1
    for i, batch in enumerate(numpy.array_split(inputs, n_chunks)):
        batch = list(batch)
        update_obj = BatchInputSimplePublicObjectBatchInput(inputs=batch)
        result = api_client.crm.contacts.batch_api.update(batch_input_simple_public_object_batch_input=update_obj)
        print(f"Batch {i}: {result.status}")


def get_notes_per_contact(api_client):
    headers = {"Authorization": f"Bearer {api_client.access_token}"}

    link = 'https://api.hubapi.com/crm/v3/objects/notes?limit=100&properties=hs_note_body,hs_timestamp&associations=contact&archived=false'

    all_notes = []
    while True:
        res = requests.get(link, headers=headers).json()
        all_notes += res['results']

        if 'paging' not in res:
            break

        link = res['paging']['next']['link']

    notes_per_contact = {}
    for note in all_notes:
        contact_assoc = note.get('associations', {}).get('contacts')
        if not contact_assoc:
            continue

        note_to_contact_assoc = [assoc_res for assoc_res in contact_assoc['results'] if
                                 assoc_res['type'] == 'note_to_contact']
        if not note_to_contact_assoc:
            continue

        contact_id = note_to_contact_assoc[0]['id']
        if contact_id not in notes_per_contact:
            notes_per_contact[contact_id] = []
        notes_per_contact[contact_id].append(note)
    return notes_per_contact


def batch_insert_notes(api_client, inputs):
    n_chunks = len(inputs) // 100 + 1
    for i, batch in enumerate(numpy.array_split(inputs, n_chunks)):
        update_obj = BatchInputSimplePublicObjectInputForCreate(inputs=list(batch))
        result = api_client.crm.objects.notes.batch_api.create(update_obj)
        print(f"Batch {i}: {result.status}")


def get_locations():
    api_client = init_api_client()
    # cohorts = ["June 2022", "October 2022", "January 2023", "March 2023", "May 2023"]
    # programs = ["Software Engineering", "Data Analytics", "Cyber Analytics", "Web Development"]

    locations = []

    programs = {
        "Software Engineering": ["January 2023"],
        "Data Analytics": ["June 2022", "October 2022", "January 2023", "March 2023", "May 2023"],
        "Cyber Analytics": ["June 2022", "January 2023", "March 2023", "May 2023"],
        # "Web Development": "Web Development"
    }

    for program, cohorts in programs.items():
        for cohort in cohorts:
            contacts = get_contacts(api_client, program, cohort,
                                    properties=['city__intercom_', 'campus_slack', 'city',
                                                'country__intercom_', 'country__front_', 'country', 'state'])
            for email, contact in contacts.items():
                city = contact.properties.get('city__intercom_', None)
                state = contact.properties.get('state', None)
                country = contact.properties.get('country__intercom_', None)

                if not city or not country:
                    continue

                location_items = [item for item in [city, state, country] if item]
                locations.append(', '.join(location_items) if location_items else '')

            locations = [location for location in locations if location]

    # remove duplicates
    location_counts = Counter(locations)
    most_common_locations = [item[0] for item in location_counts.most_common()]

    return most_common_locations


def get_hubspot_contacts_by_list_id(api_client, list_id):
    # Initialize variables
    contacts = []
    has_more = True
    vid_offset = None

    # Headers for the API request
    headers = {"Authorization": f"Bearer {api_client.access_token}"}

    # Set parameters
    properties = ['firstname',
                  'lastname',
                  'email',
                  'refund_request_status',
                  'createdate',
                  'citizenship',
                  'submitted_application___admission_status___timestamp',
                  'utm_campaign',
                  'utm_content',
                  'utm_term',
                  'utm_source',
                  'utm_id',
                  'utm_medium',
                  'utm_content',
                  'full_time_work_permit',
                  'valid_student',  # == valid work permission
                  'work_permission',
                  'gb___employment_status',
                  'paa_meeting_issue___timestamp',
                  'afa_jc_meeting_date',  # BG - AFA/JC meeting date
                  'user_feedback_survey_timestamp',  # BG - Conducted AFA/JC meeting - Timestamp
                  "BG - didn't approve - Timestamp",  # BG - didn't approve - Timestamp
                  "passed_to__october__timestamp",  # BG - doc approved - Timestamp
                  'gb___employment_status',  # BG - employment status
                  'bg___date_for_bg_approval',  # BG - estimate date for BG approval
                  'bg___date_for_bg_paper',  # BG - estimate date for BG paper
                  'bg___funnel_status',  # BG - funnel status
                  'gb___qualified',  # BG - Qualified
                  'paa_meeting_issue___timestamp',  # BG - Qualified - Timestamp
                  'bg___quit_reason',  # BG - quit reason
                  'gb___received_a_bildungsgutschein',  # BG - received a Bildungsgutschein
                  'bg___received_bg_paper___timestamp',  # BG - Received BG paper - Timestamp
                  'gb___registered_at_your_local_employment_office_or_jobcenter',
                  # BG - registered at your local Employment Office or Jobcenter
                  'bg___registered_to_eo_jc___timestamp',  # BG - Registered to EO/JC - Timestamp
                  'passed_to__january__timestamp',  # BG - Scheduled meeting with AFA/JC - Timestamp
                  'pc___hour___timestamp',  # BG - Signed the contract - Timestamp
                  'bg___submitted_typeform___timestamp',  # BG - submitted Typeform - Timestamp
                  'drop_out_students',  # BG - tasks
                  'pc_manager___timestamp',  # BG - Unqualified - Timestamp,
                  'bg___unqualified_reasons',  # BG - Unqualified reasons
                  'test_for_a_b_test',  # BG call (data)
                  'utm_campaign',
                  'utm_content',
                  'utm_id',
                  'utm_medium',
                  'utm_source',
                  'utm_term',
                  'bg0___tracking___fbc',
                  'bg0___tracking___fbp',
                  'bg0___tracking___gclid',
                  'bg0___tracking___fbclid',
                  'bg0___tracking___ttclid',
                  'bg0___tracking___ttp',
                  'bg0___age',
                  'bg___field_of_interest',
                  'bg0___field_of_interest_2',
                  'bg0___language_skill_level',
                  'bg0___german_language_skill_level',
                  'bg0___employment_situation',
                  'bg0___registered_with_the_jobcenter',
                  'bg0___state_in_germany',
                  'bg0___status_in_germany',
                  'phone',
                  'hs_analytics_first_url',
                  'submitted_application___admission_status___timestamp',
                  'admission_status_new',
                  'bg0___submitted_typeform___timestamp',
                  'bg0___voucher_status',
                  'bg___qualification_by_typeform',
                  'valid_student',
                  ]

    while has_more:
        # Build the URL
        url = f'https://api.hubapi.com/contacts/v1/lists/{list_id}/contacts/all?propertyMode=value_and_history'

        # Set parameters
        params = {
            'property': properties,
            'count': 100,  # the maximum allowed by HubSpot
        }

        if vid_offset:
            params['vidOffset'] = vid_offset

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Raise an exception if the GET request shows an error
        response.raise_for_status()

        # Get JSON response
        data = response.json()

        # Check if there are more contacts
        has_more = data['has-more']

        # Get the ID of the last contact retrieved
        if has_more:
            vid_offset = data['vid-offset']

        # Add current batch of contacts to the list
        for contact in data['contacts']:
            # Get the properties of the contact
            contact_properties = contact['properties']

            # For each property in the list, if it doesn't exist in the contact, set it to None
            for property in properties:
                if property not in contact_properties:
                    contact_properties[property] = {'value': None}

            contacts.append(contact)

    return contacts
