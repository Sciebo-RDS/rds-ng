from typing import Any, Dict, List

from datacite import schema43

from common.py.data.metadata import (Metadata, MetadataCreator, MetadataParser,
                                     MetadataParserQuery)
from common.py.data.metadata.metadata import MetadataCreator

from .utils import (parse_alternateIdentifiers, parse_contributors,
                    parse_creators, parse_dates, parse_fundingReferences,
                    parse_geoLocations, parse_publisher,
                    parse_relatedIdentifiers, parse_relatedItems, parse_rights,
                    parse_subjects)

Metadata = DataciteMetadata = List[Dict[str, Any]]


class DataciteMetadataCreator(MetadataCreator):
    
    def create(metadata: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]] = []) -> DataciteMetadata:
        datacite_metadata = MetadataParser.filter_by_profile("DataCite", metadata)

        dm = {}


# 2. creators
        creators_raw = MetadataParser.getobj(
            datacite_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/creator/"
            
        )

        dm['creators'] = parse_creators(creators_raw, shared_objects)

# 3. title
        dm['title'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/",
                "title",
            ),
        )

# 4. publisher
        publisher_raw = MetadataParser.getobj(
            datacite_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/"
            
        )

        dm['publisher'] = parse_publisher(publisher_raw, shared_objects)

# 5. publicationYear
        dm['publicationYear'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/publicationyear/",
                "publicationYear",
            ),
        )

# TODO 6. subjects

        subjects_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/"
                    
                )

        dm['subjects'] = parse_subjects(subjects_raw, shared_objects)


# 7. contributors
        contributors_raw = MetadataParser.getobj(
            datacite_metadata,
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/"
            
        )

        dm['contributors'] = parse_contributors(contributors_raw, shared_objects)



# 8. dates
        dates_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/contributor/"
                    
                )

        dm['dates'] = parse_dates(dates_raw, shared_objects)

# 9. language
        dm['language'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/language/",
                "language",
            ),
        )

# 10. resourceType 
        dm['types']['resourceType'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/resourcetype/",
                "resourceType",
            ),
        )

        dm['types']['resourceTypeGeneral'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/resourcetype/",
                "resourceTypeGeneral",
            ),
        )

# TODO 11. alternateIdentifiers
        alternateIdentifiers_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/alternateidentifier/"
                    
                )

        dm['alternateIdentifiers'] = parse_alternateIdentifiers(alternateIdentifiers_raw, shared_objects)

# TODO 12. relatedIdentifiers
        relatedIdentifiers_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relatedidentifier/"
                    
                )

        dm['relatedIdentifiers'] = parse_relatedIdentifiers(relatedIdentifiers_raw, shared_objects)

# 13. size
        dm['size'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/size/",
                "size",
            ),
        )

# 14. format
        dm['format'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/format/",
                "format",
            ),
        )

# 15. version
        dm['version'] = MetadataParser.getattr(
            datacite_metadata,
            MetadataParserQuery(
                "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/version/",
                "version",
            ),
        )

# TODO 16. rights
        rights_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/rights/"
                    
                )

        dm['rights'] = parse_rights(rights_raw, shared_objects)

# 17. description (abstract only)
        dm['descriptions'] = [
            {
                'description': MetadataParser.getattr(
                    datacite_metadata,
                    MetadataParserQuery(
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/",
                        "abstract",
                    ),
                ),
                'descriptionType': 'Abstract'
        }
        ]

# TODO 18. geoLocations
        geoLocations_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/geolocation/"
                    
                )

        dm['geoLocations'] = parse_geoLocations(geoLocations_raw, shared_objects)

# TODO 19. fundingReferences
        fundingReferences_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/fundingreference/"
                    
                )

        dm['fundingReferences'] = parse_fundingReferences(fundingReferences_raw, shared_objects)

# TODO 20. relatedItems
        relatedItems_raw = MetadataParser.getobj(
                    datacite_metadata,
                        "https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/relateditem/"
                    
                )

        dm['relatedItems'] = parse_relatedItems(relatedItems_raw, shared_objects)


        return dm