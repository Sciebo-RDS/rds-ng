import typing
from dataclasses import dataclass, field

from common.py.data.entities.resource import Resource
from ..osf import OSFProjectData, OSFStorageData

from ...base.execution import ConnectorJobTransmissionContext


@dataclass(kw_only=True)
class OSFJobTransmissionContext(ConnectorJobTransmissionContext):
    """
    A helper context to manage OSF file transmissions.
    """

    osf_project: OSFProjectData
    osf_storage: OSFStorageData
