import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { Project } from "@common/data/entities/project/Project";
import { ProjectJob } from "@common/data/entities/project/ProjectJob";

import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";

/**
 * Gets all jobs for a specific project and connector instance.
 *
 * @param project - The project.
 * @param instance - The connector instance.
 *
 * @returns A list of all matching jobs.
 */
export function getActiveProjectJob(project: Project, instance: ConnectorInstance): ProjectJob | undefined {
    const jobsStore = useProjectJobsStore();
    return jobsStore.jobs.find((job) => job.project_id == project.project_id && job.connector_instance == instance.instance_id);
}
