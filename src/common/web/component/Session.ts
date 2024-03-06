import { useSessionStorage, type RemovableRef, StorageSerializers } from "@vueuse/core";
// @ts-ignore
import { v4 as uuidv4 } from "uuid";

import { UnitID } from "../utils/UnitID";

/**
 * Class for simple session management.
 */
export class Session {
    private readonly _compID: UnitID;

    private readonly _sessionID: RemovableRef<string>;

    public constructor(compID: UnitID) {
        this._compID = compID;

        // This will generate a default session ID if none was stored yet
        this._sessionID = this.sessionValue<string>("session-id", uuidv4());
    }

    /**
     * Retrieves an arbitrary value stored for the current session.
     *
     * @param key - The value key.
     * @param defaultValue - A default value used if the value doesn't exist yet.
     * @param enforceObject - If set, the value is assumed to be an object (useful if the default value is undefined).
     *
     * @returns - The stored value or the default one otherwise.
     */
    public sessionValue<ValueType>(key: string, defaultValue: ValueType, enforceObject: boolean = false): RemovableRef<ValueType> {
        return useSessionStorage<ValueType>(`${this._compID}:${key}`, defaultValue, enforceObject ? { serializer: StorageSerializers.object } : undefined);
    }

    /**
     * The current session ID.
     */
    public get sessionID(): string {
        return this._sessionID.value;
    }
}
