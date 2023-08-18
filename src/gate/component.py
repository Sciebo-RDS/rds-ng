# pylint: disable=all
from common.py.component import (
    Component,
    COMPONENT_TYPE_INFRASTRUCTURE,
    COMPONENT_UNIT_GATE,
)
from common.py.component.roles import NodeRole
from common.py.core.messaging import Message, Event, Command, Channel, CommandReply
from common.py.service import ServiceContext
from common.py.utils import UnitID

comp = Component(
    UnitID(COMPONENT_TYPE_INFRASTRUCTURE, COMPONENT_UNIT_GATE),
    NodeRole(),
    module_name=__name__,
)
app = comp.app()
svc = comp.create_service("Gate service")

@Message.define("msg/event")
class MyEvent(Event):
    some_cool_text: str = ""
    a_number: int = 12

@svc.message_handler("msg/event", MyEvent)
def h(msg: MyEvent, ctx: ServiceContext) -> None:
    ctx.logger.info(f"EVENT: {msg.some_cool_text}, {msg.a_number}")

comp.run()
