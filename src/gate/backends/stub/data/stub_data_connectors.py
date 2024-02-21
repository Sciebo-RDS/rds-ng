import json
import typing
import uuid

from common.py.data.entities.connector import Connector, ConnectorInstance


def get_stub_data_connectors() -> typing.List[Connector]:
    """
    Adds some hardcoded data to the stub data storage.
    """

    from common.py.utils.img_conversion import convert_image_to_img_source

    from .stab_data_connector_profiles import (
        CONNECTOR_OSF_PROFILE,
        CONNECTOR_ZENODO_PROFILE,
        CONNECTOR_DATASAFE_PROFILE,
    )

    return [
        Connector(
            connector_id="osf",
            name="OpenScienceFramework",
            description="OSF connector",
            logos=Connector.Logos(
                default_logo=convert_image_to_img_source(
                    "/component/common/assets/img/logos/osf.png"
                ),
                horizontal_logo=convert_image_to_img_source(
                    "/component/common/assets/img/logos/osf.png"
                ),
            ),
            metadata_profile=json.loads(CONNECTOR_OSF_PROFILE),
        ),
        Connector(
            connector_id="datasafe",
            name="DataSafe",
            description="DataSafe connector",
            logos=Connector.Logos(
                default_logo=convert_image_to_img_source(
                    "/component/common/assets/img/logos/datasafe.png"
                ),
                horizontal_logo=convert_image_to_img_source(
                    "/component/common/assets/img/logos/datasafe.png"
                ),
            ),
            metadata_profile=json.loads(CONNECTOR_DATASAFE_PROFILE),
        ),
        Connector(
            connector_id="zenodo",
            name="Zenodo",
            description="Zenodo connector",
            logos=Connector.Logos(
                default_logo=convert_image_to_img_source(
                    "/component/common/assets/img/logos/zenodo.png"
                ),
                horizontal_logo=convert_image_to_img_source(
                    "/component/common/assets/img/logos/zenodo.png"
                ),
            ),
            metadata_profile=json.loads(CONNECTOR_ZENODO_PROFILE),
        ),
    ]


def get_stub_data_connector_instances() -> typing.List[ConnectorInstance]:
    return [
        ConnectorInstance(
            instance_id=uuid.uuid4(),
            connector_id="osf",
            name="Main OSF Account",
            description="This is our main OSF account we use to publish our excellent work.",
        ),
        ConnectorInstance(
            instance_id=uuid.uuid4(), connector_id="osf", name="Backup OSF"
        ),
        ConnectorInstance(
            instance_id=uuid.uuid4(),
            connector_id="datasafe",
            name="Backup DataSafe",
            description="Just a backup on a different service platform...",
        ),
        ConnectorInstance(
            instance_id=uuid.uuid4(),
            connector_id="osf",
            name="Long description...",
            description="This is our main OSF account we use to publish our excellent work. This is our main OSF account we use to publish our excellent work. This is our main OSF account we use to publish our excellent work.",
        ),
    ]
