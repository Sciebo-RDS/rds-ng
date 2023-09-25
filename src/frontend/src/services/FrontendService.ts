import { FrontendServiceContext } from "@/services/FrontendServiceContext";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

/**
 * Creates the main frontend service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Frontend service", (svc: Service) => {
    }, FrontendServiceContext);
}
