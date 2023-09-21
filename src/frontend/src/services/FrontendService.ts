import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

/**
 * Creates the frontend service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    return comp.createService("Frontend service");
}
