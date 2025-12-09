from dataclasses import dataclass
from typing import List

from common.py.data.entities.properties import PropertyObject


@dataclass
class DataverseAuthor:
    name: str
    affiliation: str | None = None


@dataclass
class DataversePointOfContact:
    email: str
    name: str | None = None
    affiliation: str | None = None


@dataclass
class DataverseRights:
    name: str = "CC0 1.0"
    uri: str = "https://creativecommons.org/publicdomain/zero/1.0"


def parse_authors(
    authors_raw: PropertyObject, shared_objects: List[PropertyObject]
) -> List[DataverseAuthor]:
    """
    Parses a list of datacite author data and shared objects to extract Zenodo author information.
    Args:
        authors_raw (List[Dict[str, Any]]): A list of dictionaries containing raw author references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with detailed information.
    Returns:
        List[DataverseAuthor]: A list of dictionaries, each containing parsed author information including name and affiliation.
    """

    authors: List[DataverseAuthor] = []

    if not authors_raw.refs:
        return authors

    for author_id in authors_raw.refs:
        author_raw = next((c for c in shared_objects if c.id == author_id), None)

        if not author_raw:
            continue

        name = author_raw.value.get("name", "")
        affiliation = author_raw.value.get("affiliation", None)

        authors.append(DataverseAuthor(name, affiliation))

    return authors


def parse_pocs(
    pocs_raw: PropertyObject, shared_objects: List[PropertyObject]
) -> List[DataversePointOfContact]:
    """
    Parses a list of datacite Point of Contact data and shared objects to extract Zenodo Point of Contact information.
    Args:
        pocs_raw (List[Dict[str, Any]]): A list of dictionaries containing raw Point of Contact references.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries containing shared objects with detailed information.
    Returns:
        List[DataversePointOfContact]: A list of dictionaries, each containing parsed Point of Contact information including name, affiliation and E-mail.
    """

    pocs: List[DataversePointOfContact] = []

    if not pocs_raw.refs:
        return pocs

    for poc_id in pocs_raw.refs:
        poc_raw = next((c for c in shared_objects if c.id == poc_id), None)

        if not poc_raw:
            continue

        email = poc_raw.value.get("email", "")
        name = poc_raw.value.get("name", None)
        affiliation = poc_raw.value.get("affiliation", None)

        pocs.append(DataversePointOfContact(email, name, affiliation))

    return pocs


def parse_rights(
    rights_raw: PropertyObject, shared_objects: List[PropertyObject]
) -> DataverseRights:
    """
    Parses datacite rights data and shared objects to extract Dataverse rights information.
    Args:
        rights_raw (PropertyObject): A PropertyObject containing raw rights references.
        shared_objects (List[PropertyObject]): A list of PropertyObjects containing shared objects with detailed information.
    Returns:
        DataverseRights: A rights object containing the parsed rights information.
    """

    rights = DataverseRights()

    if not rights_raw or not rights_raw.refs:
        return rights

    rights_id = next(iter(rights_raw.refs))

    rights_obj = next((r for r in shared_objects if r.id == rights_id), None)

    if not rights_obj:
        return rights

    rights.name = rights_obj.value.get("rightsIdentifier", None) or rights.name
    rights.uri = rights_obj.value.get("schemeURI", None) or rights.uri

    return rights
