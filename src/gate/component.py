import dataclasses

from common.py.component import Component, ComponentID
from common.py.core.messaging import Event, MessageName, Channel
from common.py.core.service import ServiceContext

comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()


class MyServiceContext(ServiceContext):
    pass


s = comp.create_service("Test service", context_type=MyServiceContext)


@dataclasses.dataclass(frozen=True, kw_only=True)
class MyEvent(Event):
    name: MessageName = MessageName("msg/event")
    
    some_cool_text: str = ""
    
    
@s.message_handler("msg/event", MyEvent, is_async=True)
def h(msg: MyEvent, ctx: MyServiceContext) -> None:
    ctx.logger.info(f"EVENT: {msg.some_cool_text}")
    
    
mb = comp.core.message_bus
ev = s.message_creator.create(MyEvent, Channel.local(), some_cool_text="OK SO NOICE!")
mb.dispatch(ev)
