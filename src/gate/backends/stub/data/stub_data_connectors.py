import typing
import uuid

from common.py.data.entities.connector import Connector, ConnectorInstance
from common.py.data.entities.user import UserSettings
from common.py.data.storage import StoragePool


def get_stub_data_connectors() -> typing.List[Connector]:
    """
    Adds some hardcoded data to the stub data storage.
    """

    from common.py.utils.img_conversion import convert_image_to_img_source

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
