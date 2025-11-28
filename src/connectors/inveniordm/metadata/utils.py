import datetime
import typing
from typing import Any, Dict, List

from common.py.data.entities.properties import PropertyObject


def parse_date(date: str) -> str:
    # TODO
    # FIXME
    date = datetime.datetime.fromisoformat(date) + datetime.timedelta(days=1)
    return date.strftime("%Y-%m-%d")


def parse_creators(
    creators_raw: PropertyObject, shared_objects: List[PropertyObject]
) -> List[Dict[str, Any]]:
    """
    Parses a list of datacite creator data and shared objects to extract Zenodo creator information.
    Args:
        creators_raw (List[Dict[str, Any]]): A list of dictionaries containing raw creator references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with detailed information.
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing parsed creator information including name, affiliation, ORCID, and GND identifiers.
    """
    creators = []

    if not creators_raw.refs:
        return creators

    for creator_id in creators_raw.refs:
        creator_raw = [c for c in shared_objects if c.id == creator_id][0]

        creator_person: typing.Dict[str, Any] = {"type": "personal"}
        creator_affiliations = []

        creator_objects = [e for e in shared_objects if e.id in creator_raw.refs]

        creator_person["given_name"] = creator_raw.value.get("given-name", "")
        creator_person["family_name"] = creator_raw.value.get("family-name", "")

        identifiers = []

        for obj in creator_objects:
            if obj.type == "nameIdentifier":
                scheme = obj.value.get("nameIdentifierScheme", "").lower()
                identifier = obj.value.get("nameIdentifier", "")
                identifiers.append({"scheme": scheme, "identifier": identifier})
            elif obj.type == "affiliation":
                name = obj.value.get("affiliation", "")
                creator_affiliations.append({"name": name})

        creator_person["identifiers"] = identifiers

        creators.append(
            {"person_or_org": creator_person, "affiliations": creator_affiliations}
        )

    return creators
