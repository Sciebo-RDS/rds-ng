from common.py.component import Component, ComponentID
from common.py.core.messaging import MessageName, Event, CommandReply, Command, local_channel

comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()

ev = Event(name=MessageName("msg/test"), origin=ComponentID("test", "doll"), sender=ComponentID("test", "doll"), target=local_channel())
mb = comp.core.message_bus
mb.dispatch(ev)
