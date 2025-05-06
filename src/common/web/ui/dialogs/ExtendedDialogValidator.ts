import { yupResolver } from "@primevue/forms/resolvers/yup";

import { unref } from "vue";
import { ValidationError } from "yup";
import * as yup from "yup";

/**
 * A wrapper class for form validation.
 */
export class ExtendedDialogValidator<FormType, ShapeType extends yup.ObjectShape> {
    private readonly _form: FormType;
    private readonly _resolver: any;

    private readonly _validationErrors: ValidationError[] = [];

    /**
     * @param form - The form to use.
     * @param shape - The value shape used for validation.
     */
    public constructor(form: FormType, shape: ShapeType) {
        this._form = form;
        this._resolver = yupResolver(yup.object().shape(shape));
    }

    /**
     * The resolver for the underlying form.
     */
    public get resolver(): any {
        return ({ values, name }: any) => {
            const res = this._resolver({ values, name });
            const self = this;
            // @ts-ignore
            res.then((validation) => {
                self.processValidation(validation);
            });
            return res;
        };
    }

    /**
     * Validates the form.
     *
     * @returns - A Promise that succeeds if the form is filled out correctly and fails otherwise, reporting all errors.
     */
    public validate(): Promise<void> {
        const self = this;
        return new Promise<void>(async (resolve, reject) => {
            unref(this._form)
                // @ts-ignore
                .validate()
                // @ts-ignore
                .then((validation) => {
                    self.processValidation(validation);
                    if (Object.keys(validation.errors).length == 0) {
                        resolve();
                    } else {
                        reject(self._validationErrors);
                    }
                });
        });
    }

    /**
     * Refreshes the form validation state.
     */
    public refresh(): void {
        this.validate().catch(() => {});
    }

    private processValidation(validation: any): void {
        this._validationErrors.length = 0;
        for (const [_, err] of Object.entries(validation.errors)) {
            // @ts-ignore
            this._validationErrors.push(...err);
        }
    }

    /**
     * Whether the form is currently valid.
     */
    public get isValid(): boolean {
        // @ts-ignore
        return unref(this._form)?.valid || false;
    }

    /**
     * Checks if a specific field is erroneous.
     *
     * @param field - The field to check.
     */
    public hasError(field: string): boolean {
        return this._validationErrors.find((err) => err.path === field) != undefined;
    }

    /**
     * Gets an array of all errors.
     */
    public get errors(): yup.ValidationError[] {
        return this._validationErrors;
    }

    /**
     * Gets an array of all error messages.
     */
    public get errorMessages(): string[] {
        return this._validationErrors.map((error) => error.message);
    }
}
