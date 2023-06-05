import uuid

from common.py.component import Component, ComponentID
from common.py.core.messaging import Event, Command, MessageName, Channel
from common.py.core.service import Service, ServiceContext

comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()


class EC(ServiceContext):
    pass


s = Service("Test service", context_type=EC)


@s.message_handler("msg/event", Event)
def h(msg: Event, ctx: EC) -> None:
    print(type(ctx), msg)
    ctx.logger.info("HIIIII")
    
    
@s.message_handler("msg/command", Command)
def h2(msg: Event, ctx: EC) -> None:
    print("HI COMMAND!", msg)
    ctx.logger.info("OOOOOK")
    

comp.core.register_service(s)
mb = comp.core.message_bus

ev = Event(name=MessageName("msg/event"), origin=ComponentID("test", "doll"), sender=ComponentID("test", "doll"), target=Channel.local())
mb.dispatch(ev)

cmd = Command(name=MessageName("msg/command"), origin=ComponentID("test", "supa"), sender=ComponentID("test", "supa"), target=Channel.local())
mb.dispatch(cmd)
