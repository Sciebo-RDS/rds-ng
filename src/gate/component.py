from common.py.component import Component, ComponentID
from common.py.component.roles import NodeRole
from common.py.core.messaging import Message, Event
from common.py.core.service import ServiceContext

comp = Component(ComponentID("infra", "gate"), NodeRole(), module_name=__name__)
app = comp.app()


@Message.define("msg/event")
class MyEvent(Event):
    some_cool_text: str = ""
    a_number: int = 12
    

s = comp.create_service("Test service")


@s.message_handler("msg/event", MyEvent)
def h(msg: MyEvent, ctx: ServiceContext) -> None:
    ctx.logger.info(f"EVENT: {msg.some_cool_text}, {msg.a_number}")


comp.run()
