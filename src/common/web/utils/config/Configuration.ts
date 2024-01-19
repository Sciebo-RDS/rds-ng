import { parse } from "toml";

import { SettingID } from "./SettingID";
import { deepMerge } from "../ObjectUtils";

// @ts-ignore
import configData from "/config/config.toml?url&raw";

/**
 * A general record-like object.
 */
export type SettingsContainer = Record<string, any>;

/**
 * Encapsulates configuration settings and their fallback default values.
 *
 * Settings can be loaded from a configuration file (in *TOML* format) or provided as environment variables (see below).
 *
 * All settings are accessed by an identifier of type ``SettingID``, which represents settings in a path-like format;
 * ``General.Debug``, for example, refers to a setting called ``Debug`` in the ``General` section.
 *
 * A corresponding configuration file would look like this:
 * ```
 *     [General]
 *     Debug = True
 * ```
 *
 * A setting identifier is translated to its corresponding environment variable name by replacing all dots (.) with underscores (_),
 * prepending a prefix (defaults to *'RDS'*), as well as making everything uppercase:
 * ```
 *     General.Debug -> RDS_GENERAL_DEBUG
 * ```
 *
 * Notes:
 *     When accessing a setting value, a default value must *always* be present. This means that before a setting can be accessed,
 *     a default value must be added using ``add_defaults``.
 */
export class Configuration {
    private _settings: SettingsContainer = {};
    private _defaults: SettingsContainer = {};

    private readonly _env: SettingsContainer;
    private readonly _envPrefix: string;

    /**
     * @param env - The global environment variables.
     * @param envPrefix - The prefix to use when generating the environment variable name of a setting.
     */
    public constructor(env: SettingsContainer, envPrefix: string = "RDS") {
        this._env = env;
        this._envPrefix = envPrefix;
    }

    /**
     * Loads settings from the global *TOML* configuration file.
     *
     * @throws Error - If the configuration data couldn't be parsed.
     */
    public load(): void {
        this._settings = parse(configData);
    }

    /**
     * Adds default values for settings, merging the new defaults into the existing ones.
     *
     * Notes:
     *     It is always necessary to add a default value for a setting before accessing it.
     *
     * @param defaults - A map containing the new default values.
     */
    public addDefaults(defaults: Map<SettingID, any>): void {
        for (const [key, value] of defaults.entries()) {
            let values = {};
            this.unfoldSettingsItem(key.split(), values, value);
            deepMerge(this._defaults, values);
        }
    }

    /**
     * Gets the value of a setting.
     *
     * The value is first looked up in the environment variables. If not found, the loaded settings are searched.
     * If that also fails, the defaults are used.
     *
     * @param key - The identifier of the setting.
     *
     * @returns - The value of the setting.
     *
     * @throws Error - The setting identifier was not found in the defaults.
     */
    public value<ValType = any>(key: SettingID): ValType {
        let defaultValue = this.traverseSettings(key.split(), this._defaults) as ValType;

        let envKey = key.envName(this._envPrefix);
        if (envKey in this._env) {
            return this.convertEnvType(this._env[envKey], typeof defaultValue) as ValType;
        }

        try {
            return this.traverseSettings(key.split(), this._settings) as ValType;
        } catch {
            return defaultValue;
        }
    }

    private traverseSettings(path: string[], settings: SettingsContainer): any {
        if (!(path[0] in settings)) {
            throw new Error(`Unknown settings key ${path[0]}}`);
        }
        settings = settings[path[0]];
        return path.length == 1 ? settings : this.traverseSettings(path.slice(1), settings);
    }

    private unfoldSettingsItem(path: string[], settings: SettingsContainer, value: any): void {
        if (path.length == 1) {
            settings[path[0]] = value;
        } else {
            if (!(path[0] in settings)) {
                settings[path[0]] = {};
            }

            settings = settings[path[0]];
            this.unfoldSettingsItem(path.slice(1), settings, value);
        }
    }

    private convertEnvType(value: any, targetType: string): any {
        if (targetType == "boolean") {
            if (typeof value == "string") {
                value = value.toLowerCase();
                return value == "1" || value == "yes" || value == "true";
            } else if (typeof value == "number") {
                return value > 0;
            }
        }

        return value;
    }
}
