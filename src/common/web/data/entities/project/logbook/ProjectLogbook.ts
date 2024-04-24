import { Type } from "class-transformer";

import { PublishingHistoryRecord } from "./PublishingHistoryRecord";

/**
 * Class holding all history records of a project.
 *
 * @param publishing_jobs - All running publishing jobs.
 * @para, publishing_history - All publishing history records.
 */
export class ProjectLogbook {
    // @ts-ignore
    @Type(() => PublishingHistoryRecord)
    public readonly publishing_history: PublishingHistoryRecord[];

    public constructor(publishingHistory: PublishingHistoryRecord[] = []) {
        this.publishing_history = publishingHistory;
    }
}
