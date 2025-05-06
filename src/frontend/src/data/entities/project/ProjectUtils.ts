import { ProjectJobHistoryRecord } from "@common/data/entities/project/logbook/ProjectJobHistoryRecord";
import { Project } from "@common/data/entities/project/Project";

/**
 * Gets all unseen job history records of a project.
 *
 * @param project - The project.
 *
 * @returns A list of all matching jobs.
 */
export function getUnseenProjectJobHistoryRecords(project: Project): ProjectJobHistoryRecord[] {
    return project.logbook.job_history.filter((record) => !record.seen);
}
