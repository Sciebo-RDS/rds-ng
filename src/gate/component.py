import dataclasses

from common.py.component import Component, ComponentID
from common.py.core.messaging import Event, Channel, Message, Command, CommandReply, MessageName
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
    ctx: MyServiceContext  # Just in case if the original context is needed in the callbacks
    
    
@s.message_handler("msg/event", MyEvent)
def h(msg: MyEvent, ctx: MyServiceContext) -> None:
    ctx.logger.info(f"EVENT: {msg.some_cool_text}")
    

@s.message_handler("msg/command", MyCommand)
def h2(msg: MyCommand, ctx: MyServiceContext) -> None:
    ctx.logger.info(f"COMMAND: {msg.some_number}")
    ctx.message_emitter.emit_reply(MyCommandReply, msg, success=False, message="THAT WENT WELL", ctx=ctx)
    

def h2_done(reply: MyCommandReply | None) -> None:
    print("ME GOTZ REPLY!", reply.message, reply.ctx)
    

def h2_fail(reply: MyCommandReply | None, error: str | None) -> None:
    if reply is None:
        print("I FAILED :(", error)
    else:
        print("DOOOH SUMSIN WRONG", reply)

# TODO: done-CB immer bei Reply, dann vlt mit success-Param; Fehler in fail-CB (ggf error), mit Message; unterschiedliche Typen

s.message_emitter.emit_event(MyEvent, Channel.local(), some_cool_text="OK SO NOICE!")
s.message_emitter.emit_command(MyCommand, Channel.local(), done_callback=h2_done, fail_callback=h2_fail, async_callbacks=True, some_number=123)

# This will time out
s.message_emitter.emit_command(Command, Channel.local(), done_callback=h2_done, fail_callback=h2_fail, async_callbacks=True, timeout=3.0, name=MessageName("just/a/message"))
