/**
 * Action command sent to the host.
 */
export interface HostCommunicationActionMessage {
    action: string;
    data: any;
}

/**
 * The various actions.
 */
export const enum HostCommuncationAction {
    Redirect = "redirect",
}

/**
 * Sends an action to the host (parent).
 *
 * @param action - The action to send.
 * @param data - The action data.
 */
export function sendActionToHost(action: HostCommuncationAction, data: any): void {
    window.parent.postMessage({ action: action, data: data } as HostCommunicationActionMessage, "*");
}
