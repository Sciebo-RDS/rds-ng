import uuid

from common.py.data.entities.connector import ConnectorInstance


def fill_stub_data_connectors() -> None:
    """
    Adds some hardcoded data to the stub data storage.
    """
    from ...data.storage.memory import MemoryStoragePool

    from common.py.data.entities.connector import Connector
    from common.py.utils.img_conversion import convert_image_to_img_source

    pool = (
        MemoryStoragePool()
    )  # The memory storage pool uses shared data objects, so we can fill them using a new instance

    pool.connector_storage.add(
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
        )
    )

    pool.connector_storage.add(
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
        )
    )

    pool.connector_storage.add(
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
        )
    )


def fill_stub_data_connector_instances() -> None:
    from gate.backends.stub.stub_service_context import StubServiceContext

    StubServiceContext.user_settings.connector_instances.extend(
        [
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
    )
