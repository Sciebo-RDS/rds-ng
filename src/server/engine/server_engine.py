from .project_jobs_engine import ProjectJobsEngine


class ServerEngine:
    """
    The main server engine containing all sub-engines.
    """

    def __init__(self):
        self._project_jobs_engine = ProjectJobsEngine()

    def process(self) -> None:
        """
        Performs periodic tasks.
        """
        self._project_jobs_engine.process()

    @property
    def project_jobs_engine(self) -> ProjectJobsEngine:
        """
        The project jobs engine.
        """
        return self._project_jobs_engine
