import { useComponentStore } from "../../data/stores/ComponentStore";
import { SettingID } from "./SettingID";

/**
 * Transforms a base setting ID into a host-dynamic one.
 *
 * @param key - The base setting ID.
 */
export function makeHostSettingID(key: SettingID): SettingID {
    const compStore = useComponentStore();
    return new SettingID(`${compStore.getHostInstanceID()}.${key.category}`, key.name);
}
