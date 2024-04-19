/**
 * Descriptor for a connector category.
 *
 * @param name - The category name.
 * @param description - An optional description.
 */
export class ConnectorCategory {
    public readonly name: string;
    public readonly description: string;

    protected constructor(name: string, description: string) {
        this.name = name;
        this.description = description;
    }
}
