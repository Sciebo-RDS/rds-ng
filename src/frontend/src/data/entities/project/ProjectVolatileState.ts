import { type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance.ts";
import { type ProjectID } from "@common/data/entities/project/Project.ts";
import { ProjectExternalState } from "@common/data/entities/project/ProjectExternalState.ts";

/**
 * Holds the external state for a specific project and connector instance.
 */
export class ProjectVolatileState {
    public readonly projectID: ProjectID;
    public readonly connectorInstance: ConnectorInstanceID;

    public readonly externalState: ProjectExternalState;

    public constructor(projectID: ProjectID, connectorInstance: ConnectorInstanceID, externalState: ProjectExternalState) {
        this.projectID = projectID;
        this.connectorInstance = connectorInstance;

        this.externalState = externalState;
    }
}
