from common.py.component import Component, ComponentID
from common.py.component.roles import LeafRole
from common.py.core.messaging import Event, Channel, Message

comp = Component(ComponentID("infra", "testbuddy"), LeafRole(), module_name=__name__)
app = comp.app()

svc = comp.create_service("Test buddy service")

comp.run()


@Message.define("msg/event")
class MyEvent(Event):
    some_cool_text: str = ""
    a_number: int = 12

    
svc.message_emitter.emit_event(MyEvent, Channel.direct("infra/gate/default"), some_cool_text="Wheeeee", a_number=666)
