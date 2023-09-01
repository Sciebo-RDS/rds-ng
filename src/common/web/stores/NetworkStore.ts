import { defineStore } from "pinia";
import { ref } from "vue";

/**
 * The state of the connection to the server:
 *     - **Disconnected**: No connection is established
 *     - **Connected**: A connection has been established, but no remote information has been received yet
 *     - **Ready**: The connection has been established and the remote information has been received; the connection is ready to use
 */
export const enum ConnectionState {
    Disconnected,
    Connected,
    Ready,
}

/**
 * The global store for all network-related data.
 *
 * @param connected - Whether the client is connected to a server.
 */
export const networkStore = defineStore("networkStore", () => {
    const connectionState = ref(ConnectionState.Disconnected);

    return { connectionState };
});
