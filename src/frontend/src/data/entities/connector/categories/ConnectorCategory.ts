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
    public readonly verbNoun: string;
    public readonly verbNounPlural: string;
    public readonly verbStatusProgressing: string;
    public readonly verbStatusDone: string;

    public readonly tagClass: string | undefined;
    public readonly buttonClass: string | undefined;

    protected constructor(
        name: string,
        description: string,
        verbAction: string,
        verbNoun: string,
        verbNounPlural: string,
        verbStatusProgressing: string,
        verbStatusDone: string,
        tagClass?: string,
        buttonClass?: string,
    ) {
        this.name = name;
        this.description = description;

        this.verbAction = verbAction;
        this.verbNoun = verbNoun;
        this.verbNounPlural = verbNounPlural;
        this.verbStatusProgressing = verbStatusProgressing;
        this.verbStatusDone = verbStatusDone;

        this.tagClass = tagClass;
        this.buttonClass = buttonClass;
    }
}
