from typing import Any, Dict, List


def parse_creators(creators_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parses a list of datacite creator data and shared objects to extract Zenodo creator information.
    Args:
        creators_raw (List[Dict[str, Any]]): A list of dictionaries containing raw creator references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with detailed information.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing parsed creator information including name, affiliation, ORCID, and GND identifiers.
    """
    creators = []
    for creator_id in creators_raw["refs"]:
        creator_raw = [c for c in shared_objects if c['id'] == creator_id][0]

        creator = {}
        creator_objects = [e for e in shared_objects if e['id'] in creator_raw['refs']]

        creator["name"] = creator_raw["value"].get("name", '')
        creator['affiliation'] = '; '.join([a['value'].get("affiliation", '') for a in creator_objects if a["type"] == "affiliation"])
        creator['orcid'] = '; '.join([a['value'].get("nameIdentifier", '') for a in creator_objects if a["type"] == "nameIdentifier" and a['value'].get("nameIdentifierScheme", '').lower() == "orcid"])
        creator['gnd'] = '; '.join([a['value'].get("nameIdentifier", '') for a in creator_objects if a["type"] == "nameIdentifier" and a['value'].get("nameIdentifierScheme", '').lower() == "gnd"])
        
        creators.append(creator)

    return creators

def parse_contributors(contributors_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parses a list of datacite contributor data and shared objects to extract and format contributor information for Zenodo.
    Args:
        contributors_raw (List[Dict[str, Any]]): A list of dictionaries containing raw contributor references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with detailed information.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing formatted contributor information including
                              name, type, affiliation, ORCID, and GND identifiers.
    """
    contributors = []
    for contributor_id in contributors_raw["refs"]:
        contributor_raw = [c for c in shared_objects if c['id'] == contributor_id][0]
        if contributor_raw["value"].get("nameType", '') == "Personal":

            contributor = {}
            contributor_objects = [e for e in shared_objects if e['id'] in contributor_raw['refs']]

            contributor["name"] = contributor_raw["value"].get("contributorName", '')
            contributor["type"] = contributor_raw["value"].get("contributorType", '')
            contributor['affiliation'] = '; '.join([a['value'].get("affiliation", '') for a in contributor_objects if a["type"] == "affiliation"])
            contributor['orcid'] = '; '.join([a['value'].get("nameIdentifier", '') for a in contributor_objects if a["type"] == "nameIdentifier" and a['value'].get("nameIdentifierScheme", '').lower() == "orcid"])
            contributor['gnd'] = '; '.join([a['value'].get("nameIdentifier", '') for a in contributor_objects if a["type"] == "nameIdentifier" and a['value'].get("nameIdentifierScheme", '').lower() == "gnd"])
            
            contributors.append(contributor)

    return contributors

def parse_subjects(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

""" FIXME Does not Work, Zenodo API?
    subjects = []
    for subject_id in subjects_raw["refs"]:
        subject_raw = [c for c in shared_objects if c['id'] == subject_id][0]
        
        subject = {}

        subject["term"] = subject_raw["value"].get("subject", '')
        #subject["scheme"] = subject_raw["value"].get("subjectScheme", '')
        subject["identifier"] = subject_raw["value"].get("valueURI", '')
        
        subjects.append(subject)
        
    return subjects """

def parse_grants(grants_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parses datacite grant data and returns a list of formatted Zenodo grant dictionaries.
    Args:
        grants_raw (List[Dict[str, Any]]): A list of dictionaries containing raw grant references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with grant details.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing a formatted grant with an 'id' key.
    """

    grants = []

    funder_ids = [
    "10.13039/501100002341",
    "10.13039/501100001665",
    "10.13039/100018231",
    "10.13039/501100000923",
    "10.13039/501100002428",
    "10.13039/501100000024",
    "10.13039/501100000780",
    "10.13039/501100000806",
    "10.13039/501100001871",
    "10.13039/501100004488",
    "10.13039/501100006364",
    "10.13039/501100004564",
    "10.13039/501100006588",
    "10.13039/501100000925",
    "10.13039/100000002",
    "10.13039/100000001",
    "10.13039/501100000038",
    "10.13039/501100003246",
    "10.13039/501100000690",
    "10.13039/501100001711",
    "10.13039/501100001602",
    "10.13039/100001345",
    "10.13039/501100011730",
    "10.13039/501100004410",
    "10.13039/100014013",
    "10.13039/100004440"
    ]

    for grant_id in grants_raw["refs"]:
        grant_raw = [c for c in shared_objects if c['id'] == grant_id][0]
        grant = {}
        
        if (funder_id := grant_raw["value"].get("funderIdentifier", '')) not in funder_ids or not grant_raw["value"].get("awardNumber", ''):
            continue

        grant["id"] = f"{funder_id}::{grant_raw['value'].get('awardNumber', '')}"

        grants.append(grant)


    return grants


# Hint: Zenodo API currently only allows date types Collected, Valid, Withdrawn 
def parse_dates(dates_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parses datacite date information and returns a list of formatted Zenodo date dictionaries.
    Args:
        dates_raw (List[Dict[str, Any]]): A list of dictionaries containing raw date references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with date details.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing 'start', 'end', 'type', and 'description' keys 
                              with corresponding date information.
    """

    dates = []

    for date_id in dates_raw["refs"]:
        date_raw = [c for c in shared_objects if c['id'] == date_id][0]
        
        date = {}

        date["start"] = date_raw["value"].get("date", '')[:10]
        date["end"] = date_raw["value"].get("date", '')[:10]
        date["type"] = date_raw["value"].get("dateType", '')
        date["description"] = date_raw["value"].get("dateInformation", '')
        
        dates.append(date)
        
    return dates