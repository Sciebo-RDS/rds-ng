import { AudioPreviewer } from "./previewers/AudioPreviewer";
import { ImagePreviewer } from "./previewers/ImagePreviewer";
import { PdfPreviewer } from "./previewers/PdfPreviewer";
import { TextPreviewer } from "./previewers/TextPreviewer";
import { ResourcePreviewersCatalog } from "./ResourcePreviewersCatalog";

/**
 * Registers all available resource previewers.
 *
 * When adding a new previewer, always register it here.
 */
export function registerResourcePreviewers(): void {
    // New previewers go here
    ResourcePreviewersCatalog.registerItem("images", new ImagePreviewer());
    ResourcePreviewersCatalog.registerItem("pdfs", new PdfPreviewer());
    ResourcePreviewersCatalog.registerItem("text", new TextPreviewer());
    ResourcePreviewersCatalog.registerItem("audio", new AudioPreviewer());
}
