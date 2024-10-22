import { Service } from "@common/services/Service";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the main frontend service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: FrontendComponent): Service {
    return comp.createService("Frontend service", (svc: Service) => {}, FrontendServiceContext);
}
