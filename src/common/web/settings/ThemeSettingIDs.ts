import { SettingID } from "../utils/config/SettingID";

/**
 * Identifiers for theme settings.
 *
 * @property PrimaryColor - The primary theme color (value type: ``string``).
 * @property LightSurfaceColor - The surface color when in light mode (value type: ``string``).
 * @property LightHighlightColor - The highlight color when in light mode (value type: ``string``).
 * @property DarkSurfaceColor - The surface color when in dark mode (value type: ``string``).
 * @property DarkHighlightColor - The highlight color when in dark mode (value type: ``string``).
 */
export class ThemeSettingIDs {
    public static readonly PrimaryColor = new SettingID("theme", "primary_color");

    public static readonly LightSurfaceColor = new SettingID("theme.light", "surface_color");
    public static readonly LightHighlightColor = new SettingID("theme.light", "highlight_color");

    public static readonly DarkSurfaceColor = new SettingID("theme.dark", "surface_color");
    public static readonly DarkHighlightColor = new SettingID("theme.dark", "highlight_color");
}
