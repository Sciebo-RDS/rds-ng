import { Type } from "class-transformer";

import { JobHistoryRecord } from "./JobHistoryRecord";

/**
 * Class holding all history records of a project.
 *
 * @param job_history - All job history records.
 */
export class ProjectLogbook {
    // @ts-ignore
    @Type(() => JobHistoryRecord)
    public readonly job_history: JobHistoryRecord[];

    public constructor(jobHistory: JobHistoryRecord[] = []) {
        this.job_history = jobHistory;
    }
}
