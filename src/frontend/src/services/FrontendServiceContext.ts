import { ServiceContext } from "@common/services/ServiceContext";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

/**
 * Service context for the frontend.
 *
 * Note that the store type isn't explicitely defined due to Pinia's excessive type definitions.
 */
export class FrontendServiceContext extends ServiceContext {
    private _connectorsStore = useConnectorsStore();
    private _userStore = useUserStore();
    private _projectsStore = useProjectsStore();

    /**
     * The connectors store.
     */
    public get connectorsStore() {
        return this._connectorsStore;
    }

    /**
     * The user store.
     */
    public get userStore() {
        return this._userStore;
    }

    /**
     * The projects store.
     */
    public get projectsStore() {
        return this._projectsStore;
    }
}
