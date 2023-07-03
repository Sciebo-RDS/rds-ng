import dataclasses
import typing

from .aspects import Aspects


@dataclasses.dataclass(frozen=True, kw_only=True)
class MessagingAspects(Aspects):
    message_router_type: type
    
    def create_message_router(self, *args, **kwargs):
        from ....core.messaging.routing import MessageRouter
        return typing.cast(MessageRouter, self.create_object(self.message_router_type, MessageRouter, *args, **kwargs))
