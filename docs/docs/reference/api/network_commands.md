---
sidebar_label: network_commands
title: api.network_commands
---

## PingCommand Objects

```python
@Message.define("command/general/ping")
class PingCommand(Command)
```

A generic PING command.

**Notes**:

  Requires a ``PingReply`` reply.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          chain: Message | None = None) -> CommandComposer
```

Helper function to easily build this message.

## PingReply Objects

```python
@Message.define("command/general/ping/reply")
class PingReply(CommandReply)
```

Reply to ``PingCommand``.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          cmd: PingCommand,
          *,
          success: bool = True,
          message: str = "") -> CommandReplyComposer
```

Helper function to easily build this message.

