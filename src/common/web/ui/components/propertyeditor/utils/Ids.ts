/**
 * Generates a random alphanumeric ID.
 *
 * @returns {string} The random ID.
 */
export function getRandomId(): string {
    return Math.random().toString(36).substr(2, 9);
}
