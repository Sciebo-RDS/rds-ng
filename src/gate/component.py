from common.py.component import Component, ComponentID
from common.py.core.messaging import Event, MessageName, Channel
from common.py.service import Service

comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()


s = Service("Test service")


@s.message_handler("*", Event)
def h(msg: Event) -> None:
    print("HI THERE!", msg)
    

comp.core.register_service(s)

print("LET'S GO!")
ev = Event(name=MessageName("msg/test"), origin=ComponentID("test", "doll"), sender=ComponentID("test", "doll"), target=Channel.local())
mb = comp.core.message_bus
mb.dispatch(ev)
