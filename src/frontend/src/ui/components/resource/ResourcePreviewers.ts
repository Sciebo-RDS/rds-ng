import { AudioPreviewer } from "./previewers/AudioPreviewer";
import { ImagePreviewer } from "./previewers/ImagePreviewer";
import { MarkdownPreviewer } from "./previewers/MarkdownPreviewer";
import { PdfPreviewer } from "./previewers/PdfPreviewer";
import { TextPreviewer } from "./previewers/TextPreviewer";
import { VideoPreviewer } from "./previewers/VideoPreviewer";
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
    ResourcePreviewersCatalog.registerItem("audio", new AudioPreviewer());
    ResourcePreviewersCatalog.registerItem("video", new VideoPreviewer());
    ResourcePreviewersCatalog.registerItem("markdown", new MarkdownPreviewer());
    ResourcePreviewersCatalog.registerItem("text", new TextPreviewer());
}
