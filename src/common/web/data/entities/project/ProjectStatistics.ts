import { type ConnectorInstanceID } from "../connector/ConnectorInstance";
import { JobHistoryRecordStatus } from "./logbook/JobHistoryRecord";
import { Project } from "./Project";

/**
 * Statistics about project jobs.
 */
export interface JobStatistics {
    lastJob: number;
    totalCount: {
        done: number;
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

            if (jobRecord.status == JobHistoryRecordStatus.Done) {
                this._jobStatistics[jobRecord.connector_instance].lastJob = Math.max(
                    this._jobStatistics[jobRecord.connector_instance].lastJob,
                    jobRecord.timestamp,
                );
                this._jobStatistics[jobRecord.connector_instance].totalCount.done += 1;
            } else if (jobRecord.status == JobHistoryRecordStatus.Failed) {
                this._jobStatistics[jobRecord.connector_instance].totalCount.failed += 1;
            }
        }
    }

    private createEmptyJobStatistics(): JobStatistics {
        return {
            lastJob: 0,
            totalCount: {
                done: 0,
                failed: 0,
            },
        } as JobStatistics;
    }
}
