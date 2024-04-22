import { Type } from "class-transformer";

import { ProjectHistoryRecord } from "./ProjectHistoryRecord";

/**
 * Class holding all publishing records of a project.
 *
 * @param records - All history records.
 */
export class ProjectHistory {
    // @ts-ignore
    @Type(() => ProjectHistoryRecord)
    public readonly records: ProjectHistoryRecord[];

    public constructor(records: ProjectHistoryRecord[] = []) {
        this.records = records;
    }
}
