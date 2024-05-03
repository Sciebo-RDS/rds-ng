import { type ConnectorInstanceID } from "../connector/ConnectorInstance";
import { Project } from "./Project";

/**
 * Statistics about project jobs.
 */
export interface JobStatistics {
    lastJob: number;
    totalCount: {
        succeeded: number;
        failed: number;
    };
}

/**
 * Collects various statistics about a project.
 */
export class ProjectStatistics {
    private readonly _project: Project;

    private _jobStatistics: Record<ConnectorInstanceID, JobStatistics> = {};

    public constructor(project: Project) {
        this._project = project;

        this.collectJobStatistics();
    }

    /**
     * Gets statistics about jobs of a specific connector instance.
     *
     * @param connectorInstance - The connector instance.
     */
    public getJobStatistics(connectorInstance: ConnectorInstanceID): JobStatistics {
        return connectorInstance in this._jobStatistics ? this._jobStatistics[connectorInstance] : this.createEmptyJobStatistics();
    }

    private collectJobStatistics(): void {
        this._jobStatistics = {};

        for (const jobRecord of this._project.logbook.job_history) {
            if (!(jobRecord.connector_instance in this._jobStatistics)) {
                this._jobStatistics[jobRecord.connector_instance] = this.createEmptyJobStatistics();
            }

            if (jobRecord.success) {
                this._jobStatistics[jobRecord.connector_instance].lastJob = Math.max(
                    this._jobStatistics[jobRecord.connector_instance].lastJob,
                    jobRecord.timestamp,
                );
                this._jobStatistics[jobRecord.connector_instance].totalCount.succeeded += 1;
            } else {
                this._jobStatistics[jobRecord.connector_instance].totalCount.failed += 1;
            }
        }
    }

    private createEmptyJobStatistics(): JobStatistics {
        return {
            lastJob: 0,
            totalCount: {
                succeeded: 0,
                failed: 0,
            },
        } as JobStatistics;
    }
}
