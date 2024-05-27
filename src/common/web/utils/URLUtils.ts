import { useUrlSearchParams } from "@vueuse/core";

/**
 * Retrieves a parameter from the URL query.
 *
 * @param paramName - The parameter name.
 *
 * @returns - The parameter value, if any.
 */
export function getURLQueryParam(paramName: string): string | undefined {
    const queryParams = useUrlSearchParams("history");
    return queryParams.hasOwnProperty(paramName) ? (queryParams[paramName] as string) : undefined;
}
