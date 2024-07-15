import { type ConnectorInstanceID } from "../../connector/ConnectorInstance";
import { ProjectLogbookRecord, type RecordID } from "./ProjectLogbookRecord";

/**
 * Extended data of a project job history record.
 */
export type ProjectJobHistoryRecordExtData = Record<string, any>;

/**
 * Well-known IDs of extended data entries.
 */
export const enum ProjectJobHistoryRecordExtDataIDs {
    ExternalID = "external_id",
    DOI = "doi",
}

/**
 * A single record of a project's job history.
 *
 * @param connector_instance - The connector instance ID.
 * @param status - The success status (done or failed).
 * @param message - An optional message (usually in case of an error).
 */
export class ProjectJobHistoryRecord extends ProjectLogbookRecord {
    public readonly connector_instance: ConnectorInstanceID;

    public readonly success: boolean;
    public readonly message: string;

    public readonly ext_data: ProjectJobHistoryRecordExtData;

    public constructor(
        record: RecordID,
        timestamp: number,
        connectorInstance: ConnectorInstanceID,
        success: boolean,
        message: string,
        extData: ProjectJobHistoryRecordExtData = {},
    ) {
        super(record, timestamp);

        this.connector_instance = connectorInstance;

        this.success = success;
        this.message = message;

        this.ext_data = extData;
    }
}
