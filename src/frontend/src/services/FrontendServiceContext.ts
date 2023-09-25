import { frontendStore } from "@/data/stores/FrontendStore";
import { ServiceContext } from "@common/services/ServiceContext";

/**
 * Service context for the frontend.
 *
 * Note that the store type isn't explicitely defined due to Pinia's excessive type definitions.
 */
export class FrontendServiceContext extends ServiceContext {
    private _store = frontendStore();

    /**
     * The general frontend store.
     */
    public get store() {
        return this._store;
    }
}
