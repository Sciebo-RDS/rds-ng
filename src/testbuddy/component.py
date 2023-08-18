# pylint: disable=all
from common.py.component import Component, COMPONENT_TYPE_INFRASTRUCTURE
from common.py.component.roles import LeafRole
from common.py.core.messaging import Event, Channel, Message, Command, CommandReply
from common.py.service import ServiceContext
from common.py.utils import UnitID

comp = Component(
    UnitID(COMPONENT_TYPE_INFRASTRUCTURE, "testbuddy"), LeafRole(), module_name=__name__
)
app = comp.app()
svc = comp.create_service("Test buddy service")

comp.run()
