/**
 * Descriptor for a connector category.
 *
 * @param name - The category name.
 * @param description - An optional description.
 */
export class ConnectorCategory {
    public readonly name: string;
    public readonly description: string;

    public readonly tagClass: string | undefined;

    protected constructor(name: string, description: string, tagClass?: string) {
        this.name = name;
        this.description = description;

        this.tagClass = tagClass;
    }
}
