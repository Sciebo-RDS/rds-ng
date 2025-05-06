/**
 * An interface describing constructable objects.
 */
export interface Constructable<T = object> {
    new(...args: any[]): T;
}
