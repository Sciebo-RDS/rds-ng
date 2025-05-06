/**
 * The upload state of a project.
 */
export const enum ProjectUploadState {
    Unknown = "unknown",

    Default = "default",
    Uploaded = "uploaded",
    Locked = "locked"
}

/**
 * A project's external state.
 *
 * @param external_state - The state on the external service.
 * @param external_id - The project ID within the external service.
 */
export class ProjectExternalState {
    public readonly external_state: ProjectUploadState;
    public readonly external_id: string;

    public constructor(external_state: ProjectUploadState, external_id: string) {
        this.external_state = external_state;
        this.external_id = external_id;
    }
}
