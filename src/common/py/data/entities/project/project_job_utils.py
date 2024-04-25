from .project_job import ProjectJob, ProjectJobID


def combine_project_job_id(job: ProjectJob) -> ProjectJobID:
    """
    Combines the project job keys (project ID + connector instance) to a tuple.

    Args:
        job: The project job.

    Returns:
        The ID tuple.
    """
    return job.project_id, job.connector_instance
