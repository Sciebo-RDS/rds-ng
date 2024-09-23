from dataclasses import dataclass
from typing import Any, Dict, List

from common.py.data.metadata import (Metadata, MetadataCreator, MetadataParser,
                                     MetadataParserQuery)


@dataclass
class ZenodoMetadata(Metadata):
    title: str = None
    upload_type: str = None
    description: str = None
    creators: List[Dict[str, Any]] = None
    contributors: List[Dict[str, Any]] = None


class ZenodoMetadataCreator(MetadataCreator):

    def create(metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []) -> ZenodoMetadata:

        zenodo_metadata = MetadataParser.filter_by_profile("Zenodo", metadata)

        product = ZenodoMetadata()

        product.title = MetadataParser.getattr(
            zenodo_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
                "title",
            ),
        )
        product.upload_type = MetadataParser.getattr(
            zenodo_metadata, MetadataParserQuery("ZenodoUploadType", "ZenodoUploadType")
        )
        product.description = MetadataParser.getattr(
            zenodo_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
                "abstract",
            ),
        )

        creators_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/"
            
        )

        product.creators = parse_creators(creators_raw, shared_objects)

        contributors_raw = MetadataParser.getobj(
            zenodo_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/"
            
        )

        product.contributors = parse_contributors(contributors_raw, shared_objects)

        return product
    

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