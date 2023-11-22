import { type FormContext, type GenericObject } from "vee-validate";

/**
 * A wrapper class for validation using vee-validate.
 */
export class ExtendedDialogValidator<TValues extends GenericObject = GenericObject, TOutput = TValues, FormType extends FormContext<TValues, TOutput>> {
    private readonly _form: FormType;

    /**
     * @param form - The vee-validate form to use.
     */
    public constructor(form: FormType) {
        this._form = form;
    }

    /**
     * The `defineComponentBinds` function.
     */
    public get defineComponentBinds() {
        return this._form.defineComponentBinds;
    }

    /**
     * The `handleSubmit` function.
     */
    public get handleSubmit() {
        return this._form.handleSubmit;
    }

    /**
     * A collection of all errors.
     */
    public get errors() {
        return this._form.errors;
    }
}
