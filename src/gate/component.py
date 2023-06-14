import dataclasses

from common.py.component import Component, ComponentID
from common.py.core.messaging import Event, Channel, Message, Command, CommandReply
from common.py.core.service import ServiceContext

comp = Component(ComponentID("infra", "gate"), module_name=__name__)
app = comp.wsgi_app()


class MyServiceContext(ServiceContext):
    pass


s = comp.create_service("Test service", context_type=MyServiceContext)


@Message.define("msg/event")
class MyEvent(Event):
    some_cool_text: str = ""
    
    
@Message.define("msg/command")
class MyCommand(Command):
    some_number: int = 0
    

@Message.define("msg/command/reply")
class MyCommandReply(CommandReply):
    pass
    
    
@s.message_handler("msg/event", MyEvent)
def h(msg: MyEvent, ctx: MyServiceContext) -> None:
    ctx.logger.info(f"EVENT: {msg.some_cool_text}")
    

@s.message_handler("msg/command", MyCommand)
def h2(msg: MyCommand, ctx: MyServiceContext) -> None:
    ctx.logger.info(f"COMMAND: {msg.some_number}")
    ctx.message_sender.emit_reply(MyCommandReply, msg, success=True, message="THAT WENT WELL")
    

def h2_done(reply: MyCommandReply) -> None:
    print("ME GOTZ REPLY!", reply.message)
    
    
s.message_sender.emit_event(MyEvent, Channel.local(), some_cool_text="OK SO NOICE!")
s.message_sender.emit_command(MyCommand, Channel.local(), done_callback=h2_done, some_number=123)
