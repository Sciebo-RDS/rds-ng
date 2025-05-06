import { SettingID } from "../utils/config/SettingID";

/**
 * Identifiers for theme settings.
 *
 * @property PrimaryColor - The primary theme color (value type: ``string``).
 * @property LightSurfaceColor - The surface color when in light mode (value type: ``string``).
 * @property DarkSurfaceColor - The surface color when in dark mode (value type: ``string``).
 */
export class ThemeSettingIDs {
    public static readonly PrimaryColor = new SettingID("theme", "primary_color");

    public static readonly LightSurfaceColor = new SettingID("theme.light", "surface_color");
    public static readonly DarkSurfaceColor = new SettingID("theme.dark", "surface_color");
}
