from common.py.component import Component, ComponentID
from common.py.core.messaging import MessageName, Event, CommandReply, Command, local_channel
from common.py.core.messaging.message_bus import MessageBus

comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()

ev = Event(name=MessageName("msg/test"), origin=ComponentID("test", "doll"), sender=ComponentID("test", "doll"), target=local_channel())
mb = comp.core.message_bus
mb.dispatch(ev)

@comp.core.flask.route('/')
def hello():
    return str(comp)
