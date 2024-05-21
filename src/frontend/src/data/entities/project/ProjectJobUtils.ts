import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { Project } from "@common/data/entities/project/Project";
import { ProjectJob } from "@common/data/entities/project/ProjectJob";

import { findConnectorCategoryByInstanceID } from "@/data/entities/connector/ConnectorUtils";
import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";
import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";
import { findProjectByID } from "@common/data/entities/project/ProjectUtils";

/**
 * Details about a project job.
 */
export interface ProjectJobDetails {
    project: Project | undefined;
    job: ProjectJob;
    connectorInstance: ConnectorInstance | undefined;
    connectorCategory: ConnectorCategory | undefined;
}

/**
 * Bundles information about a project job.
 *
 * @param job - The project job.
 * @param project - The project.
 * @param connectors - All connectors.
 * @param connectorInstances - All connector instances.
 */
export function getProjectJobDetails(
    job: ProjectJob,
    project: Project | undefined,
    connectors: Connector[],
    connectorInstances: ConnectorInstance[],
): ProjectJobDetails {
    return {
        project: project,
        job: job,
        connectorInstance: findConnectorInstanceByID(connectorInstances, job.connector_instance),
        connectorCategory: findConnectorCategoryByInstanceID(connectors, connectorInstances, job.connector_instance),
    } as ProjectJobDetails;
}

/**
 * Bundles information about all project jobs.
 *
 * @param projects - All projects.
 * @param jobs - All project jobs.
 * @param connectors - All connectors.
 * @param connectorInstances - All connector instances.
 */
export function getAllProjectJobDetails(
    projects: Project[],
    jobs: ProjectJob[],
    connectors: Connector[],
    connectorInstances: ConnectorInstance[],
): ProjectJobDetails[] {
    const activeJobs: ProjectJobDetails[] = [];
    jobs.forEach((job) => {
        activeJobs.push(getProjectJobDetails(job, findProjectByID(projects, job.project_id), connectors, connectorInstances));
    });
    return activeJobs.sort((a, b) => b.job.timestamp - a.job.timestamp);
}

/**
 * Gets the active job for a specific project and connector instance, if any.
 *
 * @param project - The project.
 * @param instance - The connector instance.
 *
 * @returns - The active job, if any.
 */
export function getActiveProjectJob(project: Project, instance: ConnectorInstance): ProjectJob | undefined {
    const jobsStore = useProjectJobsStore();
    return jobsStore.jobs.find((job) => job.project_id == project.project_id && job.connector_instance == instance.instance_id);
}
