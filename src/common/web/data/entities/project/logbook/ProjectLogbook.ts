import { Type } from "class-transformer";

import { ProjectJobHistoryRecord } from "./ProjectJobHistoryRecord";

/**
 * Class holding all history records of a project.
 *
 * @param job_history - All job history records.
 */
export class ProjectLogbook {
    // @ts-ignore
    @Type(() => ProjectJobHistoryRecord)
    public job_history: ProjectJobHistoryRecord[];

    public constructor(jobHistory: ProjectJobHistoryRecord[] = []) {
        this.job_history = jobHistory;
    }
}
