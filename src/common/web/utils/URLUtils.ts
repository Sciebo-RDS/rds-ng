import { useComponentStore } from "../data/stores/ComponentStore";

/**
 * Retrieves a parameter from the URL query.
 *
 * @param paramName - The parameter name.
 *
 * @returns - The parameter value, if any.
 */
export function getURLQueryParam(paramName: string): string | undefined {
    // Try to get the parameter from the actual URL, otherwise try the stored version
    const queryParams = new URLSearchParams(window.location.search);
    const compStore = useComponentStore();
    return queryParams.get(paramName) || compStore.queryParams.get(paramName) || undefined;
}
