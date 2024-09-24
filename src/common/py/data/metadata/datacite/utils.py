from typing import Any, Dict, List


def parse_creators(creators_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    creators = []
    for creator_id in creators_raw["refs"]:
        creator_raw = [c for c in shared_objects if c['id'] == creator_id][0]

        creator = {}
        creator_objects = [e for e in shared_objects if e['id'] in creator_raw['refs']]

        creator["name"] = creator_raw["value"]["name"]
        creator['affiliation'] = '; '.join([a['value']['affiliation'] for a in creator_objects if a["type"] == "affiliation"])
        creator['orcid'] = '; '.join([a['value']['nameIdentifier'] for a in creator_objects if a["type"] == "nameIdentifier" and a['value']['nameIdentifierScheme'].lower() == "orcid"])
        creator['gnd'] = '; '.join([a['value']['nameIdentifier'] for a in creator_objects if a["type"] == "nameIdentifier" and a['value']['nameIdentifierScheme'].lower() == "gnd"])
        
        creators.append(creator)

    return creators

def parse_contributors(contributors_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    contributors = []
    for contributor_id in contributors_raw["refs"]:
        contributor_raw = [c for c in shared_objects if c['id'] == contributor_id][0]
        if contributor_raw["value"]["nameType"] == "Personal":

            contributor = {}
            contributor_objects = [e for e in shared_objects if e['id'] in contributor_raw['refs']]

            contributor["name"] = contributor_raw["value"]["contributorName"]
            contributor["type"] = contributor_raw["value"]["contributorType"]
            contributor['affiliation'] = '; '.join([a['value']['affiliation'] for a in contributor_objects if a["type"] == "affiliation"])
            contributor['orcid'] = '; '.join([a['value']['nameIdentifier'] for a in contributor_objects if a["type"] == "nameIdentifier" and a['value']['nameIdentifierScheme'].lower() == "orcid"])
            contributor['gnd'] = '; '.join([a['value']['nameIdentifier'] for a in contributor_objects if a["type"] == "nameIdentifier" and a['value']['nameIdentifierScheme'].lower() == "gnd"])
            
            contributors.append(contributor)

    return contributors

def parse_publisher(publishers_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    publisher = {}

    publisher_raw = [e for e in shared_objects if e['id'] == publishers_raw[0]["refs"][0]][0]

    publisher["name"] = publisher_raw["value"]["publisher"]
    publisher["schemeUri"] = publisher_raw["value"]["schemeURI"]
    publisher["publisherIdentifier"] = publisher_raw["value"]["publisherIdentifier"]
    publisher["publisherIdentifierScheme"] = publisher_raw["value"]["publisherIdentifierScheme"]

    return publisher

def parse_dates(dates_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    dates = []

    for date_id in dates_raw["refs"]:
        date_raw = [c for c in shared_objects if c['id'] == date_id][0]

        date = {}

        date["date"] = date_raw["value"]["date"]
        date["dateType"] = date_raw["value"]["dateType"]
        date["dateInformation"] = date_raw["value"]["dateInformation"]

        dates.append(date)

    return dates

def parse_subjects(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

def parse_alternateIdentifiers(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

def parse_relatedIdentifiers(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

def parse_rights(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

def parse_geoLocations(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

def parse_fundingReferences(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass

def parse_relatedItems(subjects_raw: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pass