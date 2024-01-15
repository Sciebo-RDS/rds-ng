import { ServiceContext } from "@common/services/ServiceContext";

import { connectorsStore } from "@/data/stores/ConnectorsStore";
import { projectsStore } from "@/data/stores/ProjectsStore";
import { userStore } from "@/data/stores/UserStore";

/**
 * Service context for the frontend.
 *
 * Note that the store type isn't explicitely defined due to Pinia's excessive type definitions.
 */
export class FrontendServiceContext extends ServiceContext {
    private _connectorsStore = connectorsStore();
    private _userStore = userStore();
    private _projectsStore = projectsStore();

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
