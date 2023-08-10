/**
 * A setting identifier.
 *
 * Settings are specified by a category they belong to, as well as their actual name.
 *
 * Categories support sub-categories by separating them using dots (.);
 * when represented as a string, all component tokens are separated by dots.
 */
export class SettingID {
    public constructor(readonly category: string, readonly name: string) {
    }

    /**
     * Splits the entire identifier into single string tokens.
     *
     * @returns - The tokens list.
     */
    public split(): string[] {
        return this.toString().split(".");
    }

    /**
     * Generates an environment variable name for this identifier.
     *
     * A setting identifier is translated to its corresponding environment variable name by replacing all dots (.) with underscores (_),
     * prepending a ``prefix``, as well as making everything uppercase.
     *
     * @param prefix - prefix: The prefix to prepend.
     *
     * @returns - The corresponding environment variable name.
     */
    public envName(prefix: string): string {
        return `${prefix}_${this.toString().replace(".", "_")}`.toUpperCase();
    }

    /**
     * Converts the setting ID to a string.
     *
     * @returns - The string representation of this setting ID.
     */
    public toString(): string {
        return this.category ? `${this.category}.${this.name}` : this.name;
    }
}
