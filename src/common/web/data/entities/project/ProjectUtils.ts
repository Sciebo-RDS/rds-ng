import { Project, type ProjectID } from "./Project";

/**
 * Searches for a project by its ID within a list of projects.
 *
 * @param projects - The list of projects.
 * @param projectID - The project to search for.
 *
 * @returns - The found project or **undefined** otherwise.
 */
export function findProjectByID(projects: Project[], projectID: ProjectID): Project | undefined {
    return projects.find((project) => project.project_id == projectID);
}
