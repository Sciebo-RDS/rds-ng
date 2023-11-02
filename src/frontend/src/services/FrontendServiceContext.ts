import { projectsStore } from "@/data/stores/ProjectsStore";
import { ServiceContext } from "@common/services/ServiceContext";

/**
 * Service context for the frontend.
 *
 * Note that the store type isn't explicitely defined due to Pinia's excessive type definitions.
 */
export class FrontendServiceContext extends ServiceContext {
    private _projectStore = projectsStore();

    /**
     * The project store.
     */
    public get projectStore() {
        return this._projectStore;
    }
}
