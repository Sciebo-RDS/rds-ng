/**
 * A general unit identifier.
 *
 * A *unit* basically is something that has a unique identifier consisting of three parts: The general ``type`` (e.g., *'infra'* for components
 * belonging to the overall infrastructure), the ``unit`` name itself (e.g., *'gate'* or *'server'*), and an ``instance`` specifier (used to
 * distinguish multiple instances of the same unit).
 */
export class UnitID {
    private static readonly _delimiter = "/";

    /**
     * @param type - The unit type.
     * @param unit - The unit name.
     * @param instance - The instance specifier.
     */
    public constructor(readonly type: string, readonly unit: string, readonly instance?: string) {
    }

    /**
     * Compares this identifier to another one.
     *
     * Note that the ``instance`` specifiers are only compared if both are not ``undefined``.
     *
     * @param other - The unit identifier to compare this one to.
     *
     * @returns - Whether both identifiers are equal.
     */
    public equals(other: this): boolean {
        if (this.type !== other.type || this.unit !== other.unit) {
            return false;
        }

        if (this.instance !== undefined && other.instance !== undefined) {
            if (this.instance !== other.instance) {
                return false;
            }
        }

        return true;
    }

    /**
     * Creates a new ``UnitID`` from a string.
     *
     * The string must be of the form ``<type>/<unit>/<instance>`` or ``<type>/<unit>``.
     *
     * @param str - The unit identifier string.
     *
     * @returns - The newly created ``UnitID``.
     *
     * @throws Error - If the passed string is invalid.
     */
    public static fromString(str: string): UnitID {
        let path = str.split(UnitID._delimiter);
        switch (path.length) {
            case 2:
                return new UnitID(path[0], path[1]);

            case 3:
                return new UnitID(path[0], path[1], path[2]);

            default:
                throw new Error(`The unit ID '${str}' is invalid`);
        }
    }

    /**
     * Converts the unit ID to a string of the form ``<type>/<unit>/<instance>`` or ``<type>/<unit>``.
     */
    public toString(): string {
        return this.instance !== undefined ? [this.type, this.unit, this.instance].join(UnitID._delimiter) : [this.type, this.unit].join(UnitID._delimiter);
    }
}
