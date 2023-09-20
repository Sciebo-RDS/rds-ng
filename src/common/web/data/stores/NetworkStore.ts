import { defineStore } from "pinia";
import { ref } from "vue";
import { type ComponentInformation } from "../../api/ComponentEvents";
import { Channel } from "../../core/messaging/Channel";

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
 * @param connectionState - The client connection state.
 * @param serverInfo - If connected, general information about the server connection.
 * @param serverChannel - If connected, a ``Channel`` to directly target the connected server.
 */
export const networkStore = defineStore("networkStore", () => {
    const connectionState = ref(ConnectionState.Disconnected);

    const serverInfo = ref({} as ComponentInformation);
    const serverChannel = ref(Channel.local());

    function reset() {
        connectionState.value = ConnectionState.Disconnected;

        serverInfo.value = {} as ComponentInformation;
        serverChannel.value = Channel.local();
    }

    return {
        connectionState,
        serverInfo,
        serverChannel,
        reset
    };
});
