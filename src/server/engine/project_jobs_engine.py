from .sub_engine import SubEngine


class ProjectJobsEngine(SubEngine):
    def process(self) -> None:
        """
        Performs periodic tasks.
        """
