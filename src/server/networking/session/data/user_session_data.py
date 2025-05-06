from ....data.entities.project import ProjectVolatileStates


class UserSessionData:
    """
    User-specific (volatile) data stored in the user's session.
    """

    def __init__(self):
        self._volatile_project_states = ProjectVolatileStates()

    @property
    def volatile_project_states(self) -> ProjectVolatileStates:
        return self._volatile_project_states
