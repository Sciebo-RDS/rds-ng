import { Type } from "class-transformer";

import { ProjectHistoryRecord } from "./ProjectHistoryRecord";
import { PublishingHistoryRecord } from "./PublishingHistoryRecord";

/**
 * Class holding all history records of a project.
 *
 * @param publishing - All publishing history records.
 */
export class ProjectHistory {
    // @ts-ignore
    @Type(() => ProjectHistoryRecord)
    public readonly publishing: PublishingHistoryRecord[];

    public constructor(publishing: PublishingHistoryRecord[] = []) {
        this.publishing = publishing;
    }
}
