import { Type } from "class-transformer";

import { PublishingHistoryRecord } from "./PublishingHistoryRecord";
import { PublishingJobRecord } from "./PublishingJobRecord";

/**
 * Class holding all history records of a project.
 *
 * @param publishing_jobs - All running publishing jobs.
 * @para, publishing_history - All publishing history records.
 */
export class ProjectLogbook {
    // @ts-ignore
    @Type(() => PublishingJobRecord)
    public readonly publishing_jobs: PublishingJobRecord[];

    // @ts-ignore
    @Type(() => PublishingHistoryRecord)
    public readonly publishing_history: PublishingHistoryRecord[];

    public constructor(publishingJobs: PublishingJobRecord[] = [], publishingHistory: PublishingHistoryRecord[] = []) {
        this.publishing_jobs = publishingJobs;
        this.publishing_history = publishingHistory;
    }
}
