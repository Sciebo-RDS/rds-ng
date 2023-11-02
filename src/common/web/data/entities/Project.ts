export type ProjectID = number;

/*
 * The status of a project.
 */
export const enum ProjectStatus {
    Active = 0x0,
    Deleted = 0xff,
}

/**
 * Data for a single **Project**.
 *
 * @param project_id - The unique project identifier.
 * @param creation_time - A UNIX timestamp of the project creation time.
 * @param name - The name of the project.
 * @param description - An optional project description.
 * @param status - The project status.
 */
export class Project {
    public readonly project_id: ProjectID;

    public readonly creation_time: number;

    public readonly name: string;
    public readonly description: string;

    public readonly status: ProjectStatus = ProjectStatus.Active;

    public constructor(projectID: ProjectID, creationTime: number, name: string, description: string = "") {
        this.project_id = projectID;

        this.creation_time = creationTime;

        this.name = name;
        this.description = description;
    }
}
