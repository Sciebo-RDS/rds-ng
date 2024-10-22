import { ServiceContext } from "@common/services/ServiceContext";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useMetadataStore } from "@/data/stores/MetadataStore";
import { useProjectExportersStore } from "@/data/stores/ProjectExportersStore";
import { useProjectJobsStore } from "@/data/stores/ProjectJobsStore";
import { useProjectsStore } from "@/data/stores/ProjectsStore";
import { useUserStore } from "@/data/stores/UserStore";

/**
 * Service context for the frontend.
 *
 * Note that the store type isn't explicitely defined due to Pinia's excessive type definitions.
 */
export class FrontendServiceContext extends ServiceContext {
    private readonly _connectorsStore = useConnectorsStore();
    private readonly _metadataStore = useMetadataStore();
    private readonly _userStore = useUserStore();
    private readonly _projectsStore = useProjectsStore();
    private readonly _projectJobsStore = useProjectJobsStore();
    private readonly _projectExportersStore = useProjectExportersStore();

    /**
     * The connectors store.
     */
    public get connectorsStore() {
        return this._connectorsStore;
    }

    /**
     * The metadata store.
     */
    public get metadataStore() {
        return this._metadataStore;
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

    /**
     * The project jobs store.
     */
    public get projectJobsStore() {
        return this._projectJobsStore;
    }

    /**
     * The project exporters store.
     */
    public get projectExportersStore() {
        return this._projectExportersStore;
    }
}
