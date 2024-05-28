import { storeToRefs } from "pinia";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { BaseAuth } from "@/integration/auth/BaseAuth";

/**
 * Base authorizer.
 */
export abstract class Authorizer extends BaseAuth {
    protected constructor(comp: FrontendComponent) {
        super(comp);
    }

    /**
     * Authorize the user/integration.
     */
    public abstract authorize(): void;

    protected setAuthorized(authorized: boolean, msg: string = ""): void {
        const userStore = useUserStore();
        const { isAuthorized } = storeToRefs(userStore);

        isAuthorized.value = authorized;

        if (authorized) {
            this.callDoneCallbacks();
        } else {
            this.callFailCallbacks(msg);
        }
    }
}
