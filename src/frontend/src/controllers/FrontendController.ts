import type { FrontendComponent } from "@/component/FrontendComponent";
import { Controller } from "@common/controllers/Controller";

/**
 * Base controller for the frontend, offering additional UI helpers.
 */
export class FrontendController extends Controller {
    public constructor(comp: FrontendComponent) {
        super(comp.frontendService);
    }
}
