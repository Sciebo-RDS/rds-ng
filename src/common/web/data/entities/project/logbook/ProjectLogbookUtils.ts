import { ProjectJobHistoryRecord, ProjectJobHistoryRecordExtDataIDs } from "./ProjectJobHistoryRecord";

/**
 * Gets an entry from a project job history record's extended data.
 *
 * @param record - The project job history record.
 * @param id - The ID of the extended data entry.
 *
 * @returns - The recorded data or **undefined** otherwise.
 */
export function getJobHistoryRecordExtendedData(record: ProjectJobHistoryRecord, id: ProjectJobHistoryRecordExtDataIDs): string | undefined {
    return id in record.ext_data ? record.ext_data[ProjectJobHistoryRecordExtDataIDs.ExternalLink] : undefined;
}
