from typing import Any, Callable, Dict, List

trimDict: Callable[[dict], dict] = lambda d : {k: v for k, v in d.items() if v}

def parse_metadata(layout_objects: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Parses metadata from layout and shared objects according to the DataCite schema.
    Args:
        layout_objects (List[Dict[str, Any]]): A list of dictionaries representing layout objects.
        shared_objects (List[Dict[str, Any]]): A list of dictionaries representing shared objects.
    Returns:
        Dict[str, Any]: A dictionary containing the parsed metadata.
    """

    metadata = {"schemaVersion": "http://datacite.org/schema/kernel-4"}

    for id in ['https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/title/', 'https://datacite-metadata-schema.readthedocs.io/en/4.5/properties/description/']:
        property = [e for e in layout_objects if e['id'] == id][0]
        metadata[id.split('/')[-2:-1][0]] = [property['value']]
        layout_objects = [e for e in layout_objects if e['id'] != id]



    def parse_recursively(layout_objects: List[Dict[str, Any]], shared_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        md = {}
        for property in layout_objects:
            
            refs = parse_recursively([o for o in shared_objects if o['id'] in property['refs']], shared_objects)

            if "type" in property:
                if property["type"] not in md:
                    md[property["type"]] = []

                md[property["type"]].append(property["value"]  | refs)

            elif len(property["value"]) > 0:
                md[property["id"]] = property["value"]  | refs

            else:
                md[property["id"]] = refs

        return md

    return trimDict(parse_recursively(layout_objects, shared_objects)) | metadata
