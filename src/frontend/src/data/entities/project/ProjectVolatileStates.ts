import { type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance.ts";
import { type ProjectID } from "@common/data/entities/project/Project.ts";
import { ProjectExternalState } from "@common/data/entities/project/ProjectExternalState.ts";

import { ProjectVolatileState } from "@/data/entities/project/ProjectVolatileState.ts";

/**
 * Manages project volatile states.
 */
export class ProjectVolatileStates {
    private readonly _states: ProjectVolatileState[] = [];

    /**
     * Adds a new volatile state or updates an existing one.
     *
     * @param projectID - The project ID.
     * @param connectorInstance - The connector instance.
     * @param externalState - The external state.
     */
    public addState(projectID: ProjectID, connectorInstance: ConnectorInstanceID, externalState: ProjectExternalState): void {
        const volatileState = new ProjectVolatileState(projectID, connectorInstance, externalState);

        const currentState = this.findState(projectID, connectorInstance);
        if (!!currentState) {
            const index = this._states.indexOf(currentState);
            this._states[index] = volatileState;
        } else {
            this._states.push(volatileState);
        }
    }

    /**
     * Finds the volatile state for a certain project and connector instance.
     *
     * @param projectID - The project ID.
     * @param connectorInstance - The connector instance.
     *
     * @returns The found volatile state or **undefined** otherwise.
     */
    public findState(projectID: ProjectID, connectorInstance: ConnectorInstanceID): ProjectVolatileState | undefined {
        return this._states.find((state) => state.projectID === projectID && state.connectorInstance === connectorInstance);
    }
}
