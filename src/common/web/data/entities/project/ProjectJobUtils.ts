import { Project } from "./Project";
import { ProjectJob } from "./ProjectJob";

/**
 * Finds all active jobs of a specific project.
 *
 * @param project - The project.
 * @param jobs - All active jobs.
 *
 * @returns - All active jobs of the project.
 */
export function findProjectJobs(project: Project, jobs: ProjectJob[]): ProjectJob[] {
    return jobs.filter((job) => job.project_id == project.project_id);
}
