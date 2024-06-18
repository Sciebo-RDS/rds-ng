import { useComponentStore } from "../data/stores/ComponentStore";

/**
 * Retrieves a parameter from the URL query.
 *
 * @param paramName - The parameter name.
 *
 * @returns - The parameter value, if any.
 */
export function getURLQueryParam(paramName: string): string | undefined {
    const compStore = useComponentStore();
    return compStore.queryParams.get(paramName) || undefined;
}
