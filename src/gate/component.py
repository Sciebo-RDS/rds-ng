from common.py.component import Component, ComponentID
from common.py.component.roles import NodeRole
from common.py.core.messaging import Message, Event, Command, Channel, CommandReply
from common.py.core.service import ServiceContext

comp = Component(ComponentID("infra", "gate"), NodeRole(), module_name=__name__)
app = comp.app()


@Message.define("msg/event")
class MyEvent(Event):
    some_cool_text: str = ""
    a_number: int = 12
    
    
@Message.define("msg/command")
class MyCommand(Command):
    le_befehl: str = ""
    
    
@Message.define("msg/command/reply")
class MyCommandReply(CommandReply):
    le_reply: str = ""


s = comp.core.create_service("Test service")


def h2_done(reply: MyCommandReply, success: bool, message: str) -> None:
    print("ME GOTZ REPLY!", reply, success, message)


def h2_fail(reason: CommandReply.FailType, message: str) -> None:
    print("I FAILED :(", reason, message)


@s.message_handler("msg/event", MyEvent)
def h(msg: MyEvent, ctx: ServiceContext) -> None:
    ctx.logger.info(f"EVENT: {msg.some_cool_text}, {msg.a_number}")
    # ctx.message_emitter.emit_event(MyEvent, Channel.direct("infra/testbuddy/default"), some_cool_text="Huzaaaaa", a_number=1234)
    ctx.message_emitter.emit_command(MyCommand, Channel.direct("infra/testbuddy/default"), done_callback=h2_done, fail_callback=h2_fail, async_callbacks=True, timeout=3, le_befehl="ATTAAAACK!")
    
    
@s.message_handler("msg/command", MyCommand, is_async=True)
def h2(msg: MyCommand, ctx: ServiceContext) -> None:
    ctx.logger.info(f"COMMAND: {msg.le_befehl}")
    ctx.message_emitter.emit_reply(MyCommandReply, msg, success=False, message="THAT WENT WELL", le_reply="OUUUUI")
    

comp.run()
