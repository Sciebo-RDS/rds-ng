import { type SnapInID } from "@common/data/entities/EntityTypes";

/**
 * Frontend-specific UI settings.
 *
 * Note that this must be defined as an interface, as the actual data is stored by the backend as a non-specific dictionary.
 *
 * @param optional_snapins - A list of all user-enabled optional UI snap-ins.
 */
export interface UIOptions {
    optional_snapins: SnapInID[];
}
