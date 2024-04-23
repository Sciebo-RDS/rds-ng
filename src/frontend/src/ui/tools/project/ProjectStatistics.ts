import { type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { PublishingHistoryRecordStatus } from "@common/data/entities/project/history/PublishingHistoryRecord";
import { Project } from "@common/data/entities/project/Project";

/**
 * Statistics about project publications.
 */
export interface PublicationStatistics {
    lastPublication: number;
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

    private _publications: Record<ConnectorInstanceID, PublicationStatistics> = {};

    public constructor(project: Project) {
        this._project = project;

        this.collectPublicationStatistics();
    }

    /**
     * Gets statistics about publications of a specific connector instance.
     *
     * @param connectorInstance - The connector instance.
     */
    public getPublicationStatistics(connectorInstance: ConnectorInstanceID): PublicationStatistics {
        return connectorInstance in this._publications ? this._publications[connectorInstance] : this.createEmptyPublicationStatistics();
    }

    private collectPublicationStatistics(): void {
        this._publications = {};

        for (const publication of this._project.history.publishing) {
            if (!(publication.connector_instance in this._publications)) {
                this._publications[publication.connector_instance] = this.createEmptyPublicationStatistics();
            }

            if (publication.status == PublishingHistoryRecordStatus.Done) {
                this._publications[publication.connector_instance].lastPublication = Math.max(
                    this._publications[publication.connector_instance].lastPublication,
                    publication.timestamp,
                );
                this._publications[publication.connector_instance].totalCount.done += 1;
            } else if (publication.status == PublishingHistoryRecordStatus.Failed) {
                this._publications[publication.connector_instance].totalCount.failed += 1;
            }
        }
    }

    private createEmptyPublicationStatistics(): PublicationStatistics {
        return {
            lastPublication: 0,
            totalCount: {
                done: 0,
                failed: 0,
            },
        } as PublicationStatistics;
    }
}
