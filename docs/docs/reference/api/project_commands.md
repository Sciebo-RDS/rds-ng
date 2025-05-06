---
sidebar_label: project_commands
title: api.project_commands
---

## ListProjectsCommand Objects

```python
@Message.define("command/project/list")
class ListProjectsCommand(Command)
```

Command to fetch all projects of the current user.

**Notes**:

  Requires a ``ListProjectsReply`` reply.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          *,
          chain: Message | None = None) -> CommandComposer
```

Helper function to easily build this message.

## ListProjectsCommandReply Objects

```python
@Message.define("command/project/list/reply")
class ListProjectsCommandReply(CommandReply)
```

Reply to ``ListProjectsCommand``.

#### build

```python
@staticmethod
def build(message_builder: MessageBuilder,
          cmd: ListProjectsCommand,
          *,
          projects: typing.List[Project],
          success: bool = True,
          message: str = "") -> CommandReplyComposer
```

Helper function to easily build this message.

