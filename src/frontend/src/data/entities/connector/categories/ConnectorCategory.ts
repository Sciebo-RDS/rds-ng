/**
 * Descriptor for a connector category.
 *
 * @param name - The category name.
 * @param description - An optional description.
 */
export class ConnectorCategory {
    public readonly name: string;
    public readonly description: string;

    public readonly verbAction: string;

    public readonly tagClass: string | undefined;
    public readonly buttonClass: string | undefined;

    protected constructor(name: string, description: string, verbAction: string, tagClass?: string, buttonClass?: string) {
        this.name = name;
        this.description = description;

        this.verbAction = verbAction;

        this.tagClass = tagClass;
        this.buttonClass = buttonClass;
    }
}
