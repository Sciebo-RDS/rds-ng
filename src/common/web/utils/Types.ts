/**
 * An interface describing constructable objects.
 */
export interface Constructable {
    new(...args: any[]): object;
}
