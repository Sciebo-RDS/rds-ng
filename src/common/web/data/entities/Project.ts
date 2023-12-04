import { Type } from "class-transformer";

import { ProjectFeature } from "./ProjectFeature";

/**
 * The project ID type.
 */
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
 * @param title - The title of the project.
 * @param description - An optional project description.
 * @param status - The project status.
 * @param features - All features of the project.
 */
export class Project {
    public readonly project_id: ProjectID;

    public readonly creation_time: number;

    public readonly title: string;
    public readonly description: string;

    public readonly status: ProjectStatus = ProjectStatus.Active;

    // @ts-ignore
    @Type(() => ProjectFeature)
    public readonly features: ProjectFeature[] = [];

    public constructor(projectID: ProjectID, creationTime: number, title: string, description: string = "") {
        this.project_id = projectID;

        this.creation_time = creationTime;

        this.title = title;
        this.description = description;
    }
}
