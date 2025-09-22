from common.py.api import ProjectExternalStateEvent
from common.py.component import BackendComponent
from common.py.data.entities.project import (
    compare_external_project_states,
    get_last_known_external_project_state,
    ProjectExternalState,
)
from common.py.services import Service
from common.py.utils import EntryGuard

from ..data.types import ProjectExternalStateCallbacks


def create_projects_service(comp: BackendComponent) -> Service:
    """
    Creates the projects service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api import ProjectExternalStateRenewalEvent

    from .connector_service_context import ConnectorServiceContext

    svc = comp.create_service("Projects service", context_type=ConnectorServiceContext)

    @svc.message_handler(ProjectExternalStateRenewalEvent, is_async=True)
    def project_external_state_renewal(
        msg: ProjectExternalStateRenewalEvent, ctx: ConnectorServiceContext
    ) -> None:
        with EntryGuard(
            f"project_external_state_renewal:{msg.project.project_id}/{str(msg.connector_instance)}"
        ) as guard:
            if not guard.can_execute:
                return

            # Get the last known external project state; this can only be DEFAULT or UPLOADED
            last_external_state = get_last_known_external_project_state(
                msg.project, msg.connector_instance
            )

            def _send_external_state(external_state: ProjectExternalState) -> None:
                ProjectExternalStateEvent.build(
                    ctx.message_builder,
                    project_id=msg.project.project_id,
                    user_id=msg.user_token.user_id,
                    connector_instance=msg.connector_instance,
                    external_state=external_state,
                ).emit(ctx.remote_channel)

            # If the project has already been uploaded, update its state to reflect the actual state
            if (
                last_external_state.external_state
                == ProjectExternalState.State.UPLOADED
            ):
                callbacks = ProjectExternalStateCallbacks()
                callbacks.done(lambda state: _send_external_state(state))
                callbacks.failed(lambda _: _send_external_state(last_external_state))

                ctx.requests_handler(comp, svc).query_external_project_state(
                    msg.project,
                    msg.connector_instance,
                    msg.user_token,
                    external_state=last_external_state,
                    callbacks=callbacks,
                )
            else:
                _send_external_state(last_external_state)

    return svc
